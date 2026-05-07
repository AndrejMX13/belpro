---
source_file: "D:\Andrej\vsCode-workspace\BelPro\api\models\manager.py"
type: "code"
community: "Community None"
location: "L18"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/Community_None
---

# Manager

## Connections
- [[Approve a pending_manager log entry.]] - `uses` [INFERRED]
- [[Base]] - `uses` [INFERRED]
- [[Base_1]] - `inherits` [EXTRACTED]
- [[Best-effort email notification to volunteer after approvereject.      Silentl]] - `uses` [INFERRED]
- [[Change the manager password.  Verifies the current password before updating.]] - `uses` [INFERRED]
- [[Change the manager password.  Verifies the current password before updating._1]] - `uses` [INFERRED]
- [[Check whether an EMŠO is already registered.  Used by the frontend before form s]] - `uses` [INFERRED]
- [[Check whether an EMŠO is already registered.  Used by the frontend before form s_1]] - `uses` [INFERRED]
- [[Create a new log entry.  Volunteer must exist and be active.]] - `uses` [INFERRED]
- [[Decrypt EMŠO, mask it, and build a VolunteerResponse from an ORM object.]] - `uses` [INFERRED]
- [[Decrypt EMŠO, mask it, and build a VolunteerResponse from an ORM object._1]] - `uses` [INFERRED]
- [[Delete a pending_volunteer entry (cancelled or corrected by volunteer).]] - `uses` [INFERRED]
- [[Delete a photo. Blocked if entry is approved.]] - `uses` [INFERRED]
- [[Extract timestamp and GPS from image EXIF. All best-effort — never raises.]] - `uses` [INFERRED]
- [[FastAPI dependency — rejects requests without the correct manager password.]] - `uses` [INFERRED]
- [[Generate a monthly PDF report for one volunteer or all active volunteers.]] - `uses` [INFERRED]
- [[Generate monthly PDFs and send them via email.      Defaults to the current ca]] - `uses` [INFERRED]
- [[Generate monthly PDFs and send them via email.      Defaults to the current ca_1]] - `uses` [INFERRED]
- [[Get a single log entry by ID.]] - `uses` [INFERRED]
- [[Get a single volunteer with full log entry history (newest first).]] - `uses` [INFERRED]
- [[Get a single volunteer with full log entry history (newest first)._1]] - `uses` [INFERRED]
- [[Hard-delete a volunteer only if they have zero log entries.]] - `uses` [INFERRED]
- [[Hard-delete a volunteer only if they have zero log entries._1]] - `uses` [INFERRED]
- [[List log entries with optional filters, sorting, and pagination.]] - `uses` [INFERRED]
- [[List volunteers with optional filters, sorting, and pagination.]] - `uses` [INFERRED]
- [[List volunteers with optional filters, sorting, and pagination._1]] - `uses` [INFERRED]
- [[Log entries CRUD router — volunteer work diary entries.]] - `uses` [INFERRED]
- [[Manager authentication — HTTP Basic Auth.  Password priority   1. manager.passw]] - `uses` [INFERRED]
- [[Managers router — single-manager setup and profile.]] - `uses` [INFERRED]
- [[NGO manager.  Single row expected per deployment.]] - `rationale_for` [EXTRACTED]
- [[Re-activate a previously deactivated volunteer.]] - `uses` [INFERRED]
- [[Re-activate a previously deactivated volunteer._1]] - `uses` [INFERRED]
- [[Register a new volunteer.  Encrypts EMŠO before storing.]] - `uses` [INFERRED]
- [[Register a new volunteer.  Encrypts EMŠO before storing._1]] - `uses` [INFERRED]
- [[Registered volunteer.  Soft-deleted via active=False — never hard-deleted.]] - `uses` [INFERRED]
- [[Reject a pending_manager log entry.]] - `uses` [INFERRED]
- [[Reports router — monthly aggregation and PDF export endpoints.]] - `uses` [INFERRED]
- [[Return non-secret config status for the settings UI.]] - `uses` [INFERRED]
- [[Return per-volunteer totals of approved entries for the given yearmonth.]] - `uses` [INFERRED]
- [[Return the single manager profile, or 404 if setup has not been completed.]] - `uses` [INFERRED]
- [[Run the monthly aggregation query and return per-volunteer summaries.]] - `uses` [INFERRED]
- [[SQLAlchemy ORM models — import all to ensure they register with Base.metadata.]] - `uses` [INFERRED]
- [[Same as _to_response but includes sorted log_entries and computed hours for the]] - `uses` [INFERRED]
- [[Same as _to_response but includes sorted log_entries and computed hours for the_1]] - `uses` [INFERRED]
- [[Seed the manager profile (first-time setup). Returns 409 if already configured.]] - `uses` [INFERRED]
- [[Serve a photo file with authentication.]] - `uses` [INFERRED]
- [[Soft-delete a volunteer by setting active=False.]] - `uses` [INFERRED]
- [[Soft-delete a volunteer by setting active=False._1]] - `uses` [INFERRED]
- [[Update activity_description andor hours. Blocked once the entry is approved.]] - `uses` [INFERRED]
- [[Update manager andor NGO fields.  Only provided (non-None) fields are written.]] - `uses` [INFERRED]
- [[Update mutable fields on a volunteer (report channel preferences).]] - `uses` [INFERRED]
- [[Upload a photo for a log entry. Blocked if entry is approved.]] - `uses` [INFERRED]
- [[Volunteer]] - `uses` [INFERRED]
- [[Volunteer confirmed the entry. Transitions pending_volunteer → pending_manager.]] - `uses` [INFERRED]
- [[Volunteers CRUD router.]] - `uses` [INFERRED]
- [[create_manager()]] - `calls` [INFERRED]
- [[manager.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/INFERRED #community/Community_None