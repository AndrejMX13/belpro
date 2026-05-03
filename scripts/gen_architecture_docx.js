// Generates Belpro_Architecture.docx from scratch using docx-js.
// Run: node scripts/gen_architecture_docx.js
"use strict";

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageNumber, PageBreak, LevelFormat,
} = require("docx");
const fs = require("fs");
const path = require("path");

// ── Palette ────────────────────────────────────────────────────────────────
const TEAL       = "007878";   // section headings
const TEAL_DARK  = "1A6B6B";   // table header rows
const TEAL_MID   = "2E8B8B";   // left-column accent cells
const TEAL_LIGHT = "E0F0F0";   // alternating table rows
const WHITE      = "FFFFFF";
const DARK       = "1E2D2D";   // cover background substitute (used for cover text colour)

// ── Helpers ────────────────────────────────────────────────────────────────
const border = (color = "CCCCCC") => ({ style: BorderStyle.SINGLE, size: 1, color });
const borders = (color = "CCCCCC") => ({
  top: border(color), bottom: border(color),
  left: border(color), right: border(color),
});
const noBorders = () => ({
  top:    { style: BorderStyle.NONE },
  bottom: { style: BorderStyle.NONE },
  left:   { style: BorderStyle.NONE },
  right:  { style: BorderStyle.NONE },
});

function cell(text, opts = {}) {
  const {
    bold = false, color = "000000", fill = WHITE, shade = ShadingType.CLEAR,
    width, italic = false, fontSize = 22, align = AlignmentType.LEFT,
    vAlign = VerticalAlign.CENTER,
  } = opts;
  return new TableCell({
    borders: borders(opts.borderColor || "CCCCCC"),
    width: width ? { size: width, type: WidthType.DXA } : undefined,
    shading: { fill, type: shade },
    margins: { top: 80, bottom: 80, left: 160, right: 160 },
    verticalAlign: vAlign,
    children: [new Paragraph({
      alignment: align,
      children: [new TextRun({ text, bold, color, italics: italic, size: fontSize, font: "Arial" })],
    })],
  });
}

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: TEAL, space: 6 } },
    children: [new TextRun({ text, bold: true, size: 36, color: TEAL, font: "Arial" })],
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 80 },
    children: [new TextRun({ text, bold: true, size: 26, color: TEAL_DARK, font: "Arial" })],
  });
}

function body(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 160 },
    alignment: opts.align || AlignmentType.LEFT,
    children: [new TextRun({ text, size: 22, font: "Arial", ...opts })],
  });
}

function spacer(pts = 80) {
  return new Paragraph({ spacing: { after: pts }, children: [] });
}

// ── Tables ─────────────────────────────────────────────────────────────────

// Feature table (What is Belpro): 2-column, left col = teal label
function featureTable(rows) {
  // page content width = 11906 - 1440 - 1440 = 9026 DXA (A4 with 1 inch margins)
  const TOTAL = 9026;
  const LEFT  = 2200;
  const RIGHT = TOTAL - LEFT;
  return new Table({
    width: { size: TOTAL, type: WidthType.DXA },
    columnWidths: [LEFT, RIGHT],
    rows: rows.map(([label, desc], i) => new TableRow({
      children: [
        cell(label, { bold: true, color: WHITE, fill: TEAL_MID, width: LEFT, fontSize: 22 }),
        cell(desc,  { color: "333333", fill: i % 2 === 0 ? WHITE : TEAL_LIGHT, width: RIGHT, fontSize: 22 }),
      ],
    })),
  });
}

// Standard 3-column component table
function componentTable(headerRow, dataRows) {
  const TOTAL = 9026;
  const C1 = 2000; const C2 = 2800; const C3 = TOTAL - C1 - C2;
  return new Table({
    width: { size: TOTAL, type: WidthType.DXA },
    columnWidths: [C1, C2, C3],
    rows: [
      new TableRow({
        tableHeader: true,
        children: headerRow.map((h, i) => cell(h, {
          bold: true, color: WHITE, fill: TEAL_DARK,
          width: [C1, C2, C3][i], fontSize: 22, borderColor: TEAL_DARK,
        })),
      }),
      ...dataRows.map(([c1, c2, c3], i) => new TableRow({
        children: [
          cell(c1, { bold: true, color: TEAL_MID, fill: i % 2 === 0 ? WHITE : TEAL_LIGHT, width: C1, fontSize: 21 }),
          cell(c2, { color: "333333",              fill: i % 2 === 0 ? WHITE : TEAL_LIGHT, width: C2, fontSize: 21 }),
          cell(c3, { color: "444444",              fill: i % 2 === 0 ? WHITE : TEAL_LIGHT, width: C3, fontSize: 21 }),
        ],
      })),
    ],
  });
}

// 2-column key/value compliance table
function complianceTable(rows) {
  const TOTAL = 9026;
  const LEFT  = 2400;
  const RIGHT = TOTAL - LEFT;
  return new Table({
    width: { size: TOTAL, type: WidthType.DXA },
    columnWidths: [LEFT, RIGHT],
    rows: rows.map(([label, desc], i) => new TableRow({
      children: [
        cell(label, { bold: true, color: TEAL_MID, fill: i % 2 === 0 ? WHITE : TEAL_LIGHT, width: LEFT, fontSize: 21 }),
        cell(desc,  { color: "444444",              fill: i % 2 === 0 ? WHITE : TEAL_LIGHT, width: RIGHT, fontSize: 21 }),
      ],
    })),
  });
}

// Numbered step box (plain paragraph, styled bold label + body)
function stepParagraph(num, label, text) {
  return [
    heading2(`${num}  ${label}`),
    body(text),
    spacer(80),
  ];
}

// ── Cover page ─────────────────────────────────────────────────────────────
function coverPage() {
  return [
    spacer(2000),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 120 },
      children: [new TextRun({ text: "Belpro", bold: true, size: 72, color: TEAL, font: "Arial" })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 80 },
      children: [new TextRun({ text: "Beleženje Prostovoljstva", size: 32, color: TEAL_DARK, font: "Arial" })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 480 },
      children: [new TextRun({ text: "Digital Volunteer Diary for Slovenian NGOs", size: 28, color: "555555", font: "Arial" })],
    }),
    // Badge row — using a 4-cell table
    (() => {
      const badges = ["AI-Powered", "WhatsApp-Native", "GDPR-Compliant", "Self-Hosted"];
      const w = Math.floor(9026 / 4);
      return new Table({
        width: { size: 9026, type: WidthType.DXA },
        columnWidths: [w, w, w, 9026 - w * 3],
        rows: [new TableRow({
          children: badges.map((b, i) => cell(b, {
            bold: true, color: WHITE, fill: TEAL_MID, fontSize: 22,
            width: i < 3 ? w : 9026 - w * 3, align: AlignmentType.CENTER,
          })),
        })],
      });
    })(),
    spacer(480),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 0 },
      children: [new TextRun({ text: "Architecture & Workflow Overview · 2025", size: 22, color: "888888", font: "Arial" })],
    }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// ── Section 1: What is Belpro? ─────────────────────────────────────────────
function whatIsBelpro() {
  return [
    heading1("What is Belpro?"),
    body(
      "Belpro is a smart, AI-powered digital assistant built specifically for Slovenian non-governmental " +
      "organisations (NGOs). Its mission is simple: to make the legally required Volunteer Work Diary " +
      "(Dnevnik prostovoljskega dela) as painless as possible for everyone involved."
    ),
    body(
      "Under Slovenian law, volunteers receiving the Work Activity Allowance (Dodatek za delovno aktivnost) " +
      "must log their activities monthly and submit proof to their local Centre for Social Work (CSD). " +
      "Traditionally this meant paper forms, manual entries, and administrative overhead for the NGO. " +
      "Belpro automates the entire process — from the moment a volunteer picks up their phone to the moment " +
      "a signed PDF lands on the CSD desk."
    ),
    spacer(160),
    featureTable([
      ["Voice-first",       "Volunteers speak naturally in Slovenian — any dialect. AI does the rest."],
      ["WhatsApp",          "No new app to install. Uses the messaging platform volunteers already have."],
      ["Sovereign",         "Every NGO runs its own instance. No shared cloud, no third-party data access."],
      ["Auto-reports",      "Monthly PDF summaries generated automatically, ready for CSD submission."],
      ["Manager control",   "Every entry is reviewed and approved by the NGO manager before it is saved."],
    ]),
    spacer(240),
  ];
}

// ── Section 2: System Architecture ────────────────────────────────────────
function systemArchitecture() {
  return [
    heading1("System Architecture"),
    body(
      "Belpro is built on a modern, self-hosted microservices stack, containerised with Docker and orchestrated " +
      "locally. Every component is open-source, battle-tested, and self-hostable — no vendor lock-in, no " +
      "subscription fees, no data leaving the NGO's own infrastructure."
    ),
    body(
      "The diagram below shows the high-level data flow: volunteers communicate via WhatsApp → Evolution API " +
      "routes messages to n8n → n8n calls Whisper for transcription and writes approved records to PostgreSQL → " +
      "the manager acts via the web dashboard or WhatsApp → Gmail delivers monthly reports.",
      { italic: true, color: "666666" }
    ),
    new Paragraph({
      spacing: { after: 80 },
      children: [new TextRun({
        text: "[ Insert architecture diagram here — Fig 1 from PDF ]",
        italic: true, size: 20, color: "999999", font: "Arial",
      })],
    }),
    spacer(160),
    heading2("Core Components"),
    componentTable(
      ["Component", "Technology", "Role"],
      [
        ["Messaging layer",    "WhatsApp / Evolution API", "Real-time two-way communication with volunteers"],
        ["AI Transcription",   "Faster-Whisper",           "Converts voice notes to text, on-device, CPU-optimised"],
        ["Workflow engine",    "n8n",                      "Orchestrates all business logic — no custom glue code"],
        ["Message cache",      "Redis 7",                  "Evolution API in-memory queue and cache (required dependency)"],
        ["Database",           "PostgreSQL 18",            "Persistent, auditable storage of all volunteer records"],
        ["Web dashboard",      "FastAPI + HTML/JS",        "Manager interface for approvals, analytics and reports"],
        ["PDF engine",         "WeasyPrint",               "Generates print-ready monthly summaries"],
        ["Email delivery",     "Gmail",                    "Sends reports and notifications to volunteers"],
      ]
    ),
    spacer(240),
  ];
}

// ── Section 3: The Volunteer Journey ──────────────────────────────────────
function volunteerJourney() {
  return [
    heading1("How It Works — The Volunteer Journey"),
    body(
      "From the volunteer's perspective, Belpro feels like a simple WhatsApp chat. Behind the scenes, a " +
      "sophisticated AI pipeline captures, cleans, validates, and stores every entry with a complete audit trail."
    ),
    new Paragraph({
      spacing: { after: 80 },
      children: [new TextRun({
        text: "[ Insert 5-step workflow diagram here — Fig 2 from PDF ]",
        italic: true, size: 20, color: "999999", font: "Arial",
      })],
    }),
    spacer(160),
    ...stepParagraph(
      "①", "Record",
      "The volunteer opens WhatsApp and sends a voice note describing what they did — in plain, everyday " +
      "Slovenian. Any dialect is welcome. They can optionally attach a photo of completed work (a cleaned " +
      "room, a tended garden bed). No forms. No apps. No training required."
    ),
    ...stepParagraph(
      "②", "AI Cleans",
      "Belpro's built-in speech recognition engine (Faster-Whisper) transcribes the voice note in real time, " +
      "entirely on the NGO's own hardware. The transcript is then processed by the n8n workflow engine, which " +
      "extracts the key facts — date, hours worked, activity type, location — and structures them into a clean record."
    ),
    ...stepParagraph(
      "③", "Confirm",
      "Within seconds, the volunteer receives a neat summary back in WhatsApp: \"Date: 12 May · 3 hours · " +
      "Assisted with lunch at Dom starejših Trnovo.\" They can confirm with one tap, correct the entry if " +
      "something was misheard, or cancel entirely. The volunteer is always in control."
    ),
    ...stepParagraph(
      "④", "Manager Approval",
      "Once the volunteer confirms, the NGO manager receives an instant WhatsApp notification with the full " +
      "entry details. A single tap approves or rejects. The manager can also view and action all pending " +
      "entries via the web dashboard from any device."
    ),
    ...stepParagraph(
      "⑤", "Saved & Closed",
      "An approved entry is written to the secure database with a full timestamp. Any attached photo is stored " +
      "locally with its EXIF metadata (time and GPS location) intact — creating a tamper-evident audit trail. " +
      "The volunteer receives a friendly confirmation message."
    ),
  ];
}

// ── Section 4: Monthly Reporting ──────────────────────────────────────────
function monthlyReporting() {
  return [
    heading1("Monthly Reporting"),
    body(
      "At the end of each month, Belpro automatically generates all the paperwork the NGO needs — with zero manual effort."
    ),
    new Paragraph({
      spacing: { after: 80 },
      children: [new TextRun({
        text: "[ Insert monthly reporting cycle diagram here — Fig 3 from PDF ]",
        italic: true, size: 20, color: "999999", font: "Arial",
      })],
    }),
    spacer(160),
    heading2("Volunteer PDF"),
    body(
      "Each volunteer receives a personalised, print-ready PDF summarising their month's activities. The document " +
      "is formatted to match the CSD submission requirements — the volunteer only needs to add their signature and hand it in."
    ),
    heading2("Manager Report"),
    body(
      "The NGO manager receives a consolidated report covering all volunteers: total hours, a breakdown per " +
      "person, and flagged entries. One document, complete picture."
    ),
    heading2("Flexible Delivery"),
    body(
      "Reports can be emailed automatically (with the volunteer's consent), downloaded from the dashboard, or " +
      "printed at the NGO office. Whatever works best for the volunteer."
    ),
    spacer(240),
  ];
}

// ── Section 5: Privacy & Compliance ───────────────────────────────────────
function privacyCompliance() {
  return [
    heading1("Privacy & Compliance"),
    complianceTable([
      ["GDPR & ZVOP-2",    "All data processing complies with Slovenian and EU data protection law."],
      ["Data sovereignty", "All data stays on the NGO's own server. Nothing is sent to third parties."],
      ["Encryption",       "Sensitive personal data (EMŠO) is encrypted at rest using AES-256."],
      ["Photo privacy",    "Photos must show only work results — no faces or identifiable persons."],
      ["Retention",        "Data is kept only as long as required for CSD/IRSD inspections."],
      ["Audit trail",      "Every entry carries a complete, tamper-evident log of who approved what and when."],
    ]),
    spacer(240),
  ];
}

// ── Assemble document ──────────────────────────────────────────────────────
async function main() {
  const doc = new Document({
    styles: {
      default: {
        document: { run: { font: "Arial", size: 22, color: "222222" } },
      },
      paragraphStyles: [
        {
          id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run:       { size: 36, bold: true, color: TEAL, font: "Arial" },
          paragraph: { spacing: { before: 360, after: 120 }, outlineLevel: 0 },
        },
        {
          id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run:       { size: 26, bold: true, color: TEAL_DARK, font: "Arial" },
          paragraph: { spacing: { before: 240, after: 80 }, outlineLevel: 1 },
        },
      ],
    },
    sections: [{
      properties: {
        page: {
          size: { width: 11906, height: 16838 }, // A4
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 6 } },
            children: [
              new TextRun({ text: "Belpro", bold: true, size: 18, color: TEAL, font: "Arial" }),
              new TextRun({ text: "   —   Architecture Overview", size: 18, color: "888888", font: "Arial" }),
            ],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            border: { top: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 6 } },
            alignment: AlignmentType.RIGHT,
            children: [
              new TextRun({ text: "Page ", size: 18, color: "888888", font: "Arial" }),
              new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "888888", font: "Arial" }),
            ],
          })],
        }),
      },
      children: [
        ...coverPage(),
        ...whatIsBelpro(),
        ...systemArchitecture(),
        ...volunteerJourney(),
        ...monthlyReporting(),
        ...privacyCompliance(),
      ],
    }],
  });

  const outPath = path.join(__dirname, "..", "Belpro_Architecture.docx");
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outPath, buffer);
  console.log("Written:", outPath);
}

main().catch(err => { console.error(err); process.exit(1); });
