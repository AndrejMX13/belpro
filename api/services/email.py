"""Async email sender backed by aiosmtplib.

Reads SMTP config from the Manager row (host, port, user, from_name).
The password comes from Settings.smtp_password (stays in .env, never in DB).
"""

from __future__ import annotations

import logging
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

logger = logging.getLogger(__name__)


class SmtpNotConfiguredError(Exception):
    """Raised when the manager has not configured SMTP."""


async def send_email(
    *,
    smtp_host: str | None,
    smtp_port: int | None,
    smtp_user: str | None,
    smtp_from_name: str | None,
    smtp_password: str,
    to_address: str,
    subject: str,
    body_html: str,
    attachment_bytes: bytes | None = None,
    attachment_filename: str | None = None,
) -> None:
    """Send an email via STARTTLS SMTP.

    Raises SmtpNotConfiguredError if host/port/user are missing.
    Raises aiosmtplib.SMTPException family on delivery failure.
    """
    if not smtp_host or not smtp_port or not smtp_user:
        raise SmtpNotConfiguredError(
            "SMTP ni konfiguriran. Nastavite strežnik, vrata in uporabniško ime v Nastavitvah."
        )

    from_name = smtp_from_name or smtp_user
    from_addr = f"{from_name} <{smtp_user}>"

    if attachment_bytes and attachment_filename:
        msg: MIMEMultipart | MIMEText = MIMEMultipart()
        msg["From"] = from_addr
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body_html, "html", "utf-8"))
        part = MIMEApplication(attachment_bytes, _subtype="pdf")
        part.add_header("Content-Disposition", "attachment", filename=attachment_filename)
        msg.attach(part)
    else:
        msg = MIMEText(body_html, "html", "utf-8")
        msg["From"] = from_addr
        msg["To"] = to_address
        msg["Subject"] = subject

    await aiosmtplib.send(
        msg,
        hostname=smtp_host,
        port=smtp_port,
        username=smtp_user,
        password=smtp_password,
        start_tls=True,
    )
    logger.info("Email sent to %s | subject: %s", to_address, subject)
