# str

> 18 nodes · cohesion 0.14

## Key Concepts

- **str** (39 connections)
- **conftest.py** (6 connections) — `tests/workflow/conftest.py`
- **test_volunteer()** (5 connections) — `tests/workflow/conftest.py`
- **test_list_entries_filter_by_volunteer()** (4 connections) — `api/tests/test_log_entries.py`
- **test_get_entry_found()** (4 connections) — `api/tests/test_log_entries.py`
- **_make_valid_emso()** (4 connections) — `tests/workflow/conftest.py`
- **test_create_entry_success()** (3 connections) — `api/tests/test_log_entries.py`
- **test_create_entry_inactive_volunteer_returns_409()** (3 connections) — `api/tests/test_log_entries.py`
- **test_create_entry_missing_required_field_returns_422()** (3 connections) — `api/tests/test_log_entries.py`
- **_auth_header()** (3 connections) — `tests/workflow/conftest.py`
- **api_client()** (3 connections) — `tests/workflow/conftest.py`
- **test_create_entry_unknown_volunteer_returns_404()** (2 connections) — `api/tests/test_log_entries.py`
- **_manager_password()** (2 connections) — `tests/workflow/conftest.py`
- **n8n_client()** (2 connections) — `tests/workflow/conftest.py`
- **Generate a random 13-digit EMŠO that passes the Modulus 11 checksum.** (1 connections) — `tests/workflow/conftest.py`
- **Session-scoped AsyncClient against FastAPI. Skips all tests if unreachable.** (1 connections) — `tests/workflow/conftest.py`
- **Session-scoped AsyncClient against n8n. Skips all tests if unreachable.** (1 connections) — `tests/workflow/conftest.py`
- **Creates a volunteer with a unique phone, yields the volunteer dict,     deletes** (1 connections) — `tests/workflow/conftest.py`

## Relationships

- [[log_entry_factory()]] (8 shared connections)
- [[volunteer_factory()]] (6 shared connections)
- [[log_entries.py]] (4 shared connections)
- [[load_key()]] (4 shared connections)
- [[path]] (3 shared connections)
- [[persist_report()]] (3 shared connections)
- [[test_reports.py]] (3 shared connections)
- [[ops_server.py]] (3 shared connections)
- [[update_admin_settings()]] (2 shared connections)
- [[logo.py]] (2 shared connections)
- [[managers.py]] (2 shared connections)
- [[api/main.py]] (1 shared connections)

## Source Files

- `api/tests/test_log_entries.py`
- `tests/workflow/conftest.py`

## Audit Trail

- EXTRACTED: 33 (38%)
- INFERRED: 54 (62%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*