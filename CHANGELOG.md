# Changelog

All notable changes to BelPro are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

---

## [0.8.2] — 2026-05-08

### Removed
- 13 one-off workflow patching and deployment scripts used during early development.

## [0.8.1] — 2026-05-08

### Added
- Full WhatsApp volunteer entry flow: voice transcription → volunteer confirmation (Potrdi/Popravi/Prekliči) → manager approval via WhatsApp → email notification.
- Manager detection and routing in `volunteer_entry` workflow.
- Manager approval workflow (`manager_approval`) — WhatsApp Approve/Reject buttons.
- Test script to switch a phone number between manager and volunteer roles.
- Design spec and implementation plan for manager WhatsApp approval.

### Changed
- Updated initial database creation SQL script.
- Nginx configuration updated to prevent IP loss when API container restarts.
- Evolution API documentation updated for environment variables and API keys.
- Setup wizard updated to reflect Evolution API changes.
- Minor fixes to SPEC.md.

### Fixed
- Edit entry flow in `volunteer_entry` workflow — volunteer can now re-submit corrected entries.
- Link from Execute Workflow node to `manager_approval` workflow.
- Chrome mobile menu not working.
- Evolution API QR generation issues (see `EVOLUTION_QR_TROUBLESHOOTING.md`).

## [0.6.1] — 2026-05-04

### Added
- NGO WhatsApp number and SMTP configuration to settings.
- Analytics page with monthly analytics.
- BelPro branding fixes.
- Email service and monthly reports endpoint.
- n8n `monthly_reports` workflow.
- Approve/reject email notifications.
- `backup.sh` and `restore.sh` scripts.
- Setup wizard (`setup.sh`) for guided installation.

## [0.5.1] — 2026-05-04

### Added
- Checkboxes for monthly report preferences (manager, volunteer, global defaults).
- "Test entry" workflow documentation for testing with multiple phone numbers.

### Changed
- SPEC.md updated to reflect current code state.

## [0.4.1] — 2026-05-03

### Added
- PDF report generation (HTML→PDF via WeasyPrint) — monthly reports export.
- Reports ("Poročila") page in the dashboard.
- Dynamic back links in the UI.
- Architecture documents.

### Changed
- Cleaned Slovenian translations.
- Menu item renamed from "Odobritve" to "Dnevniki" for clarity.

### Fixed
- Nginx upload limit to allow photo uploads.
- File permissions for photo uploads.
- Removed unused environment variable references.

## [0.4.0 and earlier] — 2026-05-01 to 2026-05-03

### Added
- Project scaffold: Docker Compose services, PostgreSQL schema, FastAPI skeleton.
- Manager dashboard: login, manager record creation, volunteer management (add, search, duplicate detection, delete).
- Volunteer list with filtering, searching, sorting, re-activation.
- Log entries backend (API) and frontend (dashboard approval, lists, volunteer log list).
- Log entry detail page with photo display.
- Settings page: manager/NGO data editing and password change.
- Graphify knowledge graph tooling.
- Search and date range filtering on volunteer log list.
- MIT License and README.

---

## Changelog maintenance

To update the changelog when cutting a new release:

```bash
# Get all commits since the last version tag
git log v0.8.1..HEAD --oneline
```

Then categorize the commits under the appropriate headings and add a new section.
