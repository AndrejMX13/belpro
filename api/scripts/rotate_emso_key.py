#!/usr/bin/env python3
"""EMŠO encryption key rotation — one-off emergency tool.

Run via scripts/rotate_emso_key.sh. Do not invoke directly.

Modes:
  (no flag)        rotate: re-encrypt all EMŠOs from OLD_EMSO_KEY to NEW_EMSO_KEY
  --backup FILE    dump targeted backup (old ciphertexts + old key) to FILE
  --restore FILE   restore ciphertexts from FILE backup

Exit codes: 0 success, 1 error.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import asyncpg

from services.encryption import decrypt_emso, encrypt_emso, hash_emso, load_key
from utils.emso import emso_checksum_valid

SAMPLE_VERIFY_COUNT = 5


def _db_url() -> str:
    return os.environ["DATABASE_URL"].replace("postgresql+asyncpg://", "postgresql://")


async def cmd_backup(out_path: Path) -> None:
    """Dump volunteers table + old key to out_path as JSON."""
    old_b64 = os.environ.get("OLD_EMSO_KEY", "")
    if not old_b64:
        print("NAPAKA: OLD_EMSO_KEY ni nastavljen.", file=sys.stderr)
        sys.exit(1)
    try:
        load_key(old_b64)  # validate format before writing backup
    except ValueError as exc:
        print(f"NAPAKA: OLD_EMSO_KEY je neveljaven: {exc}", file=sys.stderr)
        sys.exit(1)

    conn = await asyncpg.connect(_db_url())
    try:
        rows = await conn.fetch(
            "SELECT id, emso, emso_hash FROM volunteers ORDER BY id"
        )
        data = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "old_key": old_b64,
            "volunteers": [
                {"id": str(r["id"]), "emso": r["emso"], "emso_hash": r["emso_hash"]}
                for r in rows
            ],
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(str(out_path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        print(f"Varnostna kopija shranjena: {out_path} ({len(rows)} zapisov)")
    finally:
        await conn.close()


async def cmd_restore(backup_path: Path) -> None:
    """Restore emso + emso_hash for all volunteers from backup_path."""
    if not backup_path.exists():
        print(f"NAPAKA: Datoteka {backup_path} ne obstaja.", file=sys.stderr)
        sys.exit(1)

    data = json.loads(backup_path.read_text(encoding="utf-8"))
    volunteers = data["volunteers"]
    old_key_b64 = data.get("old_key", "")
    backup_ids = {v["id"] for v in volunteers}

    conn = await asyncpg.connect(_db_url())
    try:
        db_rows = await conn.fetch("SELECT id FROM volunteers ORDER BY id")
        orphaned = {str(r["id"]) for r in db_rows} - backup_ids
        if orphaned:
            print(file=sys.stderr)
            print("!! OPOZORILO: NEVARNOST IZGUBE PODATKOV !!", file=sys.stderr)
            print(file=sys.stderr)
            print(
                f"V bazi je {len(orphaned)} prostovoljec/-cev, ki jih varnostna kopija ne vsebuje:",
                file=sys.stderr,
            )
            for oid in sorted(orphaned):
                print(f"  {oid}", file=sys.stderr)
            print(file=sys.stderr)
            print(
                "Po obnovi bodo ti prostovoljci šifrirani z NOVIM ključem,",
                file=sys.stderr,
            )
            print(
                "sistem pa bo preklopil na STARI ključ — njihovi EMŠO zapisi bodo NEBERLJIVI.",
                file=sys.stderr,
            )
            print(file=sys.stderr)
            answer = input("  Razumem tveganje — nadaljujem kljub temu? Vpišite 'DA': ")
            if answer.strip() != "DA":
                print("Obnovitev prekinjena.")
                sys.exit(0)
            print(file=sys.stderr)

        async with conn.transaction():
            for v in volunteers:
                await conn.execute(
                    "UPDATE volunteers SET emso = $1, emso_hash = $2 WHERE id = $3::uuid",
                    v["emso"],
                    v["emso_hash"],
                    v["id"],
                )
        print(f"Obnovljenih {len(volunteers)} zapisov iz varnostne kopije.")
        print()
        print("OPOMNIK: Posodobite EMSO_ENCRYPTION_KEY v .env na stari ključ.")
        print(f"Stari ključ preberite iz varnostne kopije: {backup_path}")
        print("Znova zaženite API vsebnik: docker compose up -d api")
    finally:
        await conn.close()


async def cmd_rotate(old_key: bytes, new_key: bytes) -> int:
    """Re-encrypt all EMŠOs from old_key to new_key. Returns count of rotated records."""
    conn = await asyncpg.connect(_db_url())
    try:
        rows = await conn.fetch("SELECT id, emso FROM volunteers ORDER BY id")

        if not rows:
            print("Ni prostovoljcev za posodobitev — zaključujem.")
            return 0

        total = len(rows)
        print(
            f"Najdenih {total} prostovoljcev. "
            "Dešifriranje in preverjanje s STARIM ključem ..."
        )

        # Phase 1: decrypt all, validate checksums — abort on first failure
        decrypted: dict[str, str] = {}
        for row in rows:
            vid = str(row["id"])
            try:
                plaintext = decrypt_emso(row["emso"], old_key)
            except Exception as exc:
                print(
                    f"NAPAKA: Dešifriranje za prostovoljca {vid} ni uspelo: {exc}",
                    file=sys.stderr,
                )
                sys.exit(1)
            if not emso_checksum_valid(plaintext):
                print(
                    f"NAPAKA: EMŠO prostovoljca {vid} ni prestalo kontrolne vsote. Prekinjam.",
                    file=sys.stderr,
                )
                sys.exit(1)
            decrypted[vid] = plaintext

        print(
            f"Vseh {total} EMŠO vrednosti dešifriranih in preverjenih. "
            "Šifriranje z NOVIM ključem ..."
        )

        # Phase 2: re-encrypt and compute new hashes
        updates: list[tuple[str, str, str]] = [
            (encrypt_emso(pt, new_key), hash_emso(pt, new_key), vid)
            for vid, pt in decrypted.items()
        ]

        # Phase 3: write all in a single atomic transaction
        async with conn.transaction():
            for new_ct, new_hash, vid in updates:
                await conn.execute(
                    "UPDATE volunteers SET emso = $1, emso_hash = $2 WHERE id = $3::uuid",
                    new_ct,
                    new_hash,
                    vid,
                )

        print(f"Vseh {total} zapisov posodobljenih v eni transakciji.")

        # Phase 4: verify sample with new key
        sample_vids = list(decrypted.keys())[:SAMPLE_VERIFY_COUNT]
        print(f"Preverjanje {len(sample_vids)} vzorčnih zapisov z NOVIM ključem ...")
        for vid in sample_vids:
            row = await conn.fetchrow(
                "SELECT emso FROM volunteers WHERE id = $1::uuid", vid
            )
            if decrypt_emso(row["emso"], new_key) != decrypted[vid]:
                print(
                    f"NAPAKA: Preverjanje ni uspelo za prostovoljca {vid}!",
                    file=sys.stderr,
                )
                print(
                    "Baza podatkov je posodobljena z novim ključem, a preverjanje je spodletelo.",
                    file=sys.stderr,
                )
                print(
                    "Uporabite --restore za obnovitev iz varnostne kopije.",
                    file=sys.stderr,
                )
                sys.exit(1)

        print(
            f"Vzorčno preverjanje uspešno. "
            f"Rotacija zaključena: {total} zapis(ov) rotiranih."
        )
        return total

    finally:
        await conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="EMSO key rotation tool")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--backup", metavar="FILE", help="Write targeted backup to FILE")
    group.add_argument("--restore", metavar="FILE", help="Restore from backup FILE")
    args = parser.parse_args()

    if args.backup:
        asyncio.run(cmd_backup(Path(args.backup)))
        return

    if args.restore:
        asyncio.run(cmd_restore(Path(args.restore)))
        return

    # Rotate mode
    old_b64 = os.environ.get("OLD_EMSO_KEY", "")
    new_b64 = os.environ.get("NEW_EMSO_KEY", "")

    if not old_b64:
        print("NAPAKA: OLD_EMSO_KEY ni nastavljen.", file=sys.stderr)
        sys.exit(1)
    if not new_b64:
        print("NAPAKA: NEW_EMSO_KEY ni nastavljen.", file=sys.stderr)
        sys.exit(1)
    if old_b64 == new_b64:
        print("NAPAKA: Oba ključa sta enaka — ni kaj zavrteti.", file=sys.stderr)
        sys.exit(1)

    try:
        old_key = load_key(old_b64)
    except ValueError as exc:
        print(f"NAPAKA: OLD_EMSO_KEY je neveljaven: {exc}", file=sys.stderr)
        sys.exit(1)
    try:
        new_key = load_key(new_b64)
    except ValueError as exc:
        print(f"NAPAKA: NEW_EMSO_KEY je neveljaven: {exc}", file=sys.stderr)
        sys.exit(1)

    asyncio.run(cmd_rotate(old_key, new_key))


if __name__ == "__main__":
    main()
