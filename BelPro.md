# Digital Volunteer Diary: System Architecture & Specification

## 1. Project Overview
The **Digital Volunteer Diary** is a sovereign, low-cost, AI-powered solution for Slovenian NGOs [cite: 1]. It automates the "Volunteering Diaries" (*Dnevnik prostovoljskega dela*) required for recipients of social support, providing a robust audit trail to prevent abuse [cite: 1].

## 2. Technical Architecture
*   **Interface:** WhatsApp (Evolution API) [cite: 1].
*   **Transcription:** Faster-Whisper (CPU optimized) [cite: 1].
*   **Logic:** n8n Workflow [cite: 1].
*   **Database:** PostgreSQL (Self-hosted) [cite: 1].

## 3. GDPR Notes for Volunteer Agreements
To ensure compliance with **ZVOP-2** and **GDPR**, NGOs should add the following clauses to their standard Volunteer Agreement (*Dogovor o prostovoljstvu*):

### Article X: Digital Record Keeping and Privacy
1. **Purpose of Collection:** The Volunteer agrees to use the WhatsApp-based reporting system to log hours. This data (voice notes, text, and photos) is collected solely to fulfill legal reporting obligations for the Work Activity Allowance (*Dodatek za delovno aktivnost*) [cite: 1, 2].
2. **Photo Evidence Protocol:** When submitting photo evidence of completed tasks, the Volunteer shall ensure that **no faces or identifiable persons** are visible. The focus must be strictly on the result of the work (e.g., cleaned premises, completed garden beds) [cite: 2].
3. **Metadata and Verification:** The Volunteer acknowledges that photo metadata (timestamp and location) will be stored as part of the audit trail to verify the authenticity of the work performed [cite: 2].
4. **Data Retention:** Photos and logs will be stored in the NGO's secure local database for as long as required by state inspections (CSD/IRSD). Data will not be shared with third parties except for official audit purposes [cite: 2].

## 4. Operational Flow
*   **Volunteer:** Sends Voice Note + Photo [cite: 2].
*   **AI:** Normalizes dialect and extracts structured data [cite: 1, 2].
*   **Manager:** Approves the entry via a simple WhatsApp button [cite: 1, 2].
