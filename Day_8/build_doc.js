const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, AlignmentType, PageBreak, LevelFormat,
  convertInchesToTwip
} = require("docx");

// ---------------------------------------------------------
// Helper functions to keep the document-building code readable
// ---------------------------------------------------------

function heading1(text) {
  return new Paragraph({
    text: text,
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 400, after: 200 },
  });
}

function heading2(text) {
  return new Paragraph({
    text: text,
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 300, after: 150 },
  });
}

function heading3(text) {
  return new Paragraph({
    text: text,
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 100 },
  });
}

function body(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, ...opts })],
    spacing: { after: 150 },
  });
}

function bullet(text) {
  return new Paragraph({
    text: text,
    bullet: { level: 0 },
    spacing: { after: 80 },
  });
}

function labelValuePara(label, value) {
  return new Paragraph({
    children: [
      new TextRun({ text: label + ": ", bold: true }),
      new TextRun({ text: value }),
    ],
    spacing: { after: 80 },
  });
}

// A styled table cell for our 7-field use case tables
function fieldCell(text, isHeader = false) {
  return new TableCell({
    width: { size: 2800, type: WidthType.DXA },
    shading: isHeader ? { type: ShadingType.CLEAR, fill: "1F4E5F" } : undefined,
    children: [
      new Paragraph({
        children: [
          new TextRun({
            text: text,
            bold: isHeader,
            color: isHeader ? "FFFFFF" : "000000",
          }),
        ],
      }),
    ],
    margins: { top: 100, bottom: 100, left: 100, right: 100 },
  });
}

function valueCell(text) {
  return new TableCell({
    width: { size: 7100, type: WidthType.DXA },
    children: [new Paragraph({ text: text })],
    margins: { top: 100, bottom: 100, left: 100, right: 100 },
  });
}

// Builds one full 7-row use case table
function useCaseTable(fields) {
  const rows = [
    ["Problem Statement", fields.problem],
    ["Proposed AI Solution", fields.solution],
    ["Input Data Required", fields.inputData],
    ["Expected Output", fields.output],
    ["AI/ML Technology", fields.technology],
    ["Possible API/Model", fields.apiModel],
    ["Where It Will Be Integrated", fields.integration],
  ];

  return new Table({
    width: { size: 9900, type: WidthType.DXA },
    columnWidths: [2800, 7100],
    rows: rows.map(
      ([label, value]) =>
        new TableRow({
          children: [fieldCell(label, true), valueCell(value)],
        })
    ),
  });
}

// Simple text-based architecture flow box (User -> App -> AI Service -> Model/API -> Response)
function architectureFlow(steps) {
  const paras = [];
  steps.forEach((step, i) => {
    paras.push(
      new Paragraph({
        children: [
          new TextRun({ text: `${i + 1}. `, bold: true, size: 24 }),
          new TextRun({ text: step.title, bold: true, size: 24 }),
        ],
        spacing: { before: 150, after: 40 },
      })
    );
    paras.push(
      new Paragraph({
        children: [new TextRun({ text: step.detail, italics: true, size: 21 })],
        spacing: { after: 100 },
        indent: { left: 400 },
      })
    );
    if (i < steps.length - 1) {
      paras.push(
        new Paragraph({
          children: [new TextRun({ text: "        ↓", size: 28, bold: true })],
          spacing: { after: 100 },
        })
      );
    }
  });
  return paras;
}

// ---------------------------------------------------------
// Document content
// ---------------------------------------------------------

const doc = new Document({
  sections: [
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 }, // US Letter
          margin: {
            top: convertInchesToTwip(1),
            bottom: convertInchesToTwip(1),
            left: convertInchesToTwip(1),
            right: convertInchesToTwip(1),
          },
        },
      },
      children: [
        // ---------------- COVER ----------------
        new Paragraph({
          children: [new TextRun({ text: "HisabDo AI/ML Capstone Project", bold: true, size: 44 })],
          spacing: { before: 800, after: 200 },
          alignment: AlignmentType.CENTER,
        }),
        new Paragraph({
          children: [new TextRun({ text: "Day 8 Task — AI/ML Track", size: 28, italics: true })],
          alignment: AlignmentType.CENTER,
          spacing: { after: 100 },
        }),
        new Paragraph({
          children: [new TextRun({ text: "Remote Internship Program", size: 24 })],
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
        }),
        new Paragraph({
          children: [new TextRun({ text: "Prepared by: Abbas Raza", size: 22, bold: true })],
          alignment: AlignmentType.CENTER,
          spacing: { after: 60 },
        }),
        new Paragraph({
          children: [new TextRun({ text: "GitHub: github.com/AbbasRaza5055/Hisabdo", size: 20 })],
          alignment: AlignmentType.CENTER,
          spacing: { after: 60 },
        }),
        new Paragraph({
          children: [new TextRun({ text: "Product analyzed: HisabDo (hisabdo.app)", size: 20 })],
          alignment: AlignmentType.CENTER,
          spacing: { after: 600 },
        }),

        new Paragraph({ children: [new PageBreak()] }),

        // ---------------- 1. INTRODUCTION ----------------
        heading1("1. Introduction & Objective"),
        body(
          "This document analyzes HisabDo — a digital khata/ledger application built for shopkeepers, freelancers, wholesalers, and home-based sellers in Pakistan — and identifies practical, grounded opportunities where AI and Machine Learning can add real value to the website, web application, and mobile application."
        ),
        body(
          "Rather than proposing generic fintech AI features, every use case in this document is grounded in HisabDo's actual product: its offline-first design, its existing voice-entry feature, its multi-language support (Urdu, Roman Urdu, Hindi, Arabic), and its real user personas. This document also incorporates direct feedback gathered from a hands-on user of the app (see Section 4)."
        ),

        // ---------------- 2. PRODUCT EXPLORATION ----------------
        heading1("2. Product Exploration"),
        heading2("2.1 What HisabDo Is"),
        body(
          "HisabDo is a mobile and web-based digital khata (ledger) application that replaces the traditional paper udhar/khata notebook used by small businesses across Pakistan. It allows users to record customer credit (udhar), track payments, generate PDF statements, and manage day-to-day business transactions — all with offline-first functionality so it works reliably without a stable internet connection."
        ),
        heading2("2.2 Target Users (Personas)"),
        bullet("Corner shop / retail owners — tracking dozens of regular customers' running credit balances"),
        bullet("Freelancers — tracking client payments and outstanding invoices"),
        bullet("Wholesalers — tracking payables to suppliers alongside receivables from retail customers"),
        bullet("Home-based sellers — tracking informal, often cash-based sales and customer credit"),
        heading2("2.3 Existing Features Observed"),
        bullet("Voice-based transaction entry (in supported languages)"),
        bullet("PDF export of ledger/statement records"),
        bullet("Multi-language interface: Urdu, Roman Urdu, Hindi, Arabic"),
        bullet("Offline-first data entry, designed for low/unreliable connectivity environments"),
        bullet("Recently added cloud sync (per the app's most recent update notes)"),
        heading2("2.4 User Workflow (Typical)"),
        bullet("User opens the app and selects a customer/contact, or adds a new one"),
        bullet("User records a transaction (credit given, or payment received) — via manual entry or voice"),
        bullet("The running balance for that customer updates automatically"),
        bullet("User can export a PDF statement to share with the customer or for their own records"),
        bullet("User checks the dashboard for an overview of total receivables across all customers"),

        // ---------------- 3. AI/ML USE CASES ----------------
        heading1("3. Identified AI/ML Use Cases"),
        body(
          "The following five use cases were selected because each addresses a real, observable gap in the current product — not a generic AI feature disconnected from how HisabDo is actually used."
        ),

        // --- Use Case 1 ---
        heading2("3.1 Use Case 1: Smart Reminders for Overdue Udhar"),
        useCaseTable({
          problem:
            "Shopkeepers currently must manually remember and decide when to follow up with customers who have outstanding credit (udhar). With dozens of customers, overdue balances are easy to lose track of, leading to delayed or missed collections.",
          solution:
            "An AI-driven reminder engine that analyzes each customer's payment history and outstanding balance to predict which customers are likely to become overdue, then proactively suggests (or automatically schedules) a reminder — rather than relying on simple fixed-date reminders alone.",
          inputData:
            "Historical transaction records per customer (dates, amounts, payment patterns), current outstanding balance, average days-to-repay per customer, optional due-date if set by the user.",
          output:
            "A prioritized list of customers to follow up with, an estimated 'risk of non-payment' indicator, and a suggested reminder message (auto-generated, editable) in the user's preferred language.",
          technology:
            "Classical Machine Learning (classification/scoring model) — e.g., Logistic Regression or Gradient Boosting (XGBoost/LightGBM) trained on repayment-timing patterns. Does not require deep learning given the tabular, structured nature of the data.",
          apiModel:
            "Custom-trained lightweight model (scikit-learn / LightGBM), deployable via a small FastAPI microservice — similar in spirit to the model-serving pattern built in Day 7 of this internship. No third-party API strictly required, though a notification-delivery API (e.g., Firebase Cloud Messaging) would be needed to actually send the reminder.",
          integration:
            "Mobile Application (primary — push notifications), Web Application (dashboard alert widget). Not applicable to the marketing website.",
        }),

        // --- Use Case 2 ---
        heading2("3.2 Use Case 2: OCR Receipt / Bill Scanner"),
        useCaseTable({
          problem:
            "Currently, transactions can only be entered manually or via voice. For wholesalers and shopkeepers who receive paper invoices or handwritten bills from suppliers, there is no way to quickly digitize that paperwork — it must be re-typed by hand, which is slow and error-prone.",
          solution:
            "An OCR (Optical Character Recognition) feature that lets a user photograph a paper receipt or invoice, automatically extracts the vendor name, date, amount, and line items, and pre-fills a new transaction entry for the user to confirm.",
          inputData:
            "A photo of a receipt/invoice/bill, taken via the phone camera or uploaded from gallery.",
          output:
            "A structured, editable transaction draft: vendor/customer name, amount, date, and (where possible) itemized line items — ready for one-tap confirmation instead of full manual entry.",
          technology:
            "Computer Vision + OCR pipeline: image preprocessing (deskew, denoise — similar to techniques used in this internship's earlier OCR work) followed by text recognition, then a lightweight NLP/regex-based extraction layer to identify amount, date, and vendor fields from raw OCR text.",
          apiModel:
            "Google ML Kit Text Recognition (on-device, works offline — a strong fit for HisabDo's offline-first design) or Tesseract OCR for a self-hosted option. Cloud alternative: Google Cloud Vision API or AWS Textract, if online-only processing is acceptable.",
          integration:
            "Mobile Application (primary — camera access), Web Application (secondary — file upload only, no camera). Not applicable to the marketing website.",
        }),

        // --- Use Case 3 ---
        heading2("3.3 Use Case 3: Smart Expense / Transaction Categorization"),
        useCaseTable({
          problem:
            "All transactions are currently recorded without any automatic categorization (e.g., inventory purchase, utility bill, customer sale). Without categories, users cannot see spending/earning patterns by type, which limits the usefulness of reports and insights.",
          solution:
            "An AI model that automatically suggests a category for each new transaction based on the description/notes entered (via text or voice-to-text), learning from the user's own correction patterns over time to improve personalization.",
          inputData:
            "Transaction description/notes text (from manual or voice entry), transaction amount, and the user's own history of past category corrections (for personalization).",
          output:
            "A suggested category label (e.g., 'Inventory', 'Utility Bill', 'Customer Sale', 'Supplier Payment') attached to each transaction automatically, editable by the user with one tap.",
          technology:
            "NLP text classification. Given HisabDo's multi-language support (Urdu, Roman Urdu, Hindi, Arabic), a multilingual transformer-based embedding model is preferred over a classical bag-of-words approach, since it generalizes better across mixed-language, informal text.",
          apiModel:
            "Multilingual Sentence Embeddings (e.g., 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', used previously in this internship's Customer Support Agent project) combined with a simple classifier head, or a hosted LLM API (e.g., Groq's Llama models) prompted for zero-shot categorization to avoid training a custom model initially.",
          integration:
            "Mobile Application (primary), Web Application (primary — same categorization logic applies). Not applicable to the marketing website.",
        }),

        // --- Use Case 4 ---
        heading2("3.4 Use Case 4: AI Financial Insights (Cash Flow Health Summary)"),
        useCaseTable({
          problem:
            "Users can see individual transactions and balances, but HisabDo does not currently translate that raw data into a simple, plain-language understanding of overall business health — most users are not accountants and don't intuitively read ledger totals as trends.",
          solution:
            "A periodic (weekly/monthly) AI-generated plain-language summary: total receivables vs. payables, which customers/categories are driving the biggest changes, and simple, actionable observations (e.g., 'Udhar from 3 customers has been outstanding for over 30 days').",
          inputData:
            "Aggregated transaction history over the reporting period, customer-level balance changes, category breakdowns (if Use Case 3 is implemented).",
          output:
            "A short, plain-language written summary (in the user's preferred language) plus 2-3 simple supporting charts (e.g., balance trend, top overdue customers).",
          technology:
            "A combination of statistical aggregation (trend/summary statistics, no ML required for the numbers themselves) and a Large Language Model used specifically for natural-language generation of the summary text from those statistics.",
          apiModel:
            "Statistics computed with Pandas (server-side or on-device); summary text generated via a hosted LLM API such as Groq (Llama 3.3 70B — already used successfully in this internship's Customer Support Agent project) or Google Gemini's free tier.",
          integration:
            "Mobile Application (primary — dashboard card), Web Application (primary — dashboard/reports section). Not applicable to the marketing website.",
        }),

        // --- Use Case 5 ---
        heading2("3.5 Use Case 5: Voice-Based AI Query Assistant"),
        useCaseTable({
          problem:
            "HisabDo already supports voice for entering transactions, but users cannot currently ask the app questions using voice (e.g., 'Ahmed ka kitna udhar baaki hai?' — 'How much does Ahmed still owe?'). This means users must manually search and read the screen even for simple lookups.",
          solution:
            "Extend the existing voice feature from one-directional data entry into a two-directional voice assistant: users can ask natural-language questions about their ledger and receive a spoken or on-screen answer.",
          inputData:
            "Voice audio input (converted to text), the user's transaction/customer database to query against.",
          output:
            "A direct spoken and/or text answer to the user's question (e.g., a specific balance, a list of overdue customers, a total for the week).",
          technology:
            "Speech-to-Text, followed by intent detection and entity extraction (identifying which customer/date-range/metric is being asked about) — conceptually similar to the intent-detection pipeline already built in this internship's LangGraph-based Customer Support Agent — then a database query, then Text-to-Speech for the spoken response.",
          apiModel:
            "On-device Speech-to-Text (Android SpeechRecognizer / Google ML Kit) for offline reliability; intent parsing via a small hosted LLM (Groq) or a rule-based/regex fallback for common query patterns; Text-to-Speech via Android's built-in TTS engine.",
          integration:
            "Mobile Application (primary — voice is a mobile-native interaction). Limited applicability to Web Application (browser microphone access possible but less natural). Not applicable to the marketing website.",
        }),

        // ---------------- 4. USER FEEDBACK ----------------
        heading1("4. User Feedback"),
        body(
          "The app was installed and used hands-on as part of this task. The feedback below reflects a genuine, direct experience with the application, and directly informed the prioritization of the Top 2 features in Section 5."
        ),
        heading2("4.1 What Worked Well"),
        bullet("The dashboard/overview gave a clear, at-a-glance picture of overall balances."),
        bullet("PDF export was genuinely useful for sharing statements."),
        bullet("Voice entry worked well for logging transactions quickly."),
        bullet("Overall, the app felt simple and easy to use — low learning curve."),
        heading2("4.2 Friction Points"),
        bullet(
          "No AI or smart assistance anywhere in the app — every workflow (entry, categorization, follow-up) is fully manual, even where the app already has the underlying data to do more."
        ),
        bullet("Login had some issues during setup (a usability/reliability gap, separate from the AI opportunities but worth noting)."),
        heading2("4.3 Most-Wanted Improvement"),
        body(
          "The single most-requested improvement was smart reminders for overdue udhar — directly validating Use Case 1 (Section 3.1) as a genuine, user-driven priority rather than an assumption.",
          { italics: true }
        ),
        body(
          "Note: this feedback reflects one direct, hands-on user (the author of this report). A fuller version of this activity would involve gathering structured feedback from at least five distinct users across HisabDo's core personas (shopkeeper, freelancer, wholesaler, home-based seller) to validate these priorities more broadly.",
          { size: 20, italics: true, color: "666666" }
        ),

        // ---------------- 5. TOP 2 ARCHITECTURE ----------------
        heading1("5. Top 2 Features — Technical Architecture"),
        body(
          "Based on the AI research (Section 3) and real user feedback (Section 4), the following two features were selected for a deeper technical architecture: Smart Reminders for Overdue Udhar (directly requested by the user) and OCR Receipt/Bill Scanner (highest technical depth and clearest fit with HisabDo's offline-first design)."
        ),

        heading2("5.1 Architecture: Smart Reminders for Overdue Udhar"),
        ...architectureFlow([
          {
            title: "User",
            detail:
              "Shopkeeper opens the app; in the background, no direct action is needed for this feature to run periodically.",
          },
          {
            title: "Application (Mobile/Web)",
            detail:
              "On a scheduled interval (e.g., daily background job), the app sends each customer's transaction history and current balance to the AI Service.",
          },
          {
            title: "AI Service",
            detail:
              "A lightweight FastAPI microservice (same pattern as Day 7 of this internship) receives the data, applies feature engineering (days since last payment, average repayment time, balance size), and calls the trained model.",
          },
          {
            title: "Model/API",
            detail:
              "A scikit-learn / LightGBM classification model (self-hosted, not a third-party API) scores each customer's likelihood of becoming overdue and returns a ranked list with confidence scores.",
          },
          {
            title: "Response",
            detail:
              "The app receives the ranked list, generates a suggested reminder message per customer, and either sends a push notification (via Firebase Cloud Messaging) or surfaces an in-app alert card for the user to review and send.",
          },
        ]),

        heading2("5.2 Architecture: OCR Receipt / Bill Scanner"),
        ...architectureFlow([
          {
            title: "User",
            detail:
              "User taps 'Scan Receipt' and photographs a paper bill/invoice using the phone camera.",
          },
          {
            title: "Application (Mobile)",
            detail:
              "The app preprocesses the image on-device (crop, deskew, contrast adjustment) before passing it forward.",
          },
          {
            title: "AI Service",
            detail:
              "On-device OCR (Google ML Kit Text Recognition) runs first for offline reliability. If the result confidence is low, the app can optionally fall back to a cloud OCR call when internet is available.",
          },
          {
            title: "Model/API",
            detail:
              "Extracted raw text is passed through a lightweight parsing layer (regex + simple NLP rules) to identify amount, date, and vendor name from the unstructured OCR output.",
          },
          {
            title: "Response",
            detail:
              "A pre-filled, editable transaction draft is shown to the user for one-tap confirmation, instead of requiring full manual data entry.",
          },
        ]),

        // ---------------- 6. IMPLEMENTATION EXPLANATION ----------------
        heading1("6. Short Implementation Explanation"),
        body(
          "Both Top 2 features are intentionally designed to fit HisabDo's existing constraints rather than assume a different product. Specifically:"
        ),
        bullet(
          "Offline-first compatibility: The OCR feature is designed to run on-device first (Google ML Kit), matching HisabDo's offline-first philosophy, with cloud OCR only as an optional fallback."
        ),
        bullet(
          "Lightweight, not resource-heavy: The Smart Reminders model is a classical ML model (not deep learning), which keeps hosting costs low and inference fast — appropriate for an early-stage app."
        ),
        bullet(
          "Builds on existing infrastructure: Both features reuse patterns already proven in this internship (FastAPI model-serving from Day 7, OCR preprocessing techniques from earlier project work), reducing implementation risk."
        ),
        bullet(
          "Multi-language aware: Any user-facing AI text (reminder messages, category labels) should respect HisabDo's existing multi-language support (Urdu, Roman Urdu, Hindi, Arabic) rather than assuming English-only output."
        ),
        body(
          "A realistic phased rollout would begin with Smart Reminders (lower technical complexity, directly requested by users, and deployable using the same FastAPI pattern from Day 7), followed by the OCR Receipt Scanner (higher complexity due to on-device computer vision integration, but high perceived value for wholesaler and shopkeeper personas who handle paper invoices)."
        ),

        // ---------------- 7. CONCLUSION ----------------
        heading1("7. Conclusion"),
        body(
          "HisabDo's core strength is its simplicity and offline-first reliability for small business owners who need a fast, low-friction alternative to a paper khata notebook. The AI opportunities identified in this document are deliberately designed to extend that strength rather than compete with it — automating the parts of the workflow (reminders, categorization, data entry from paper) that are currently manual and repetitive, while preserving the simplicity that makes the app usable for non-technical users in the first place."
        ),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  require("fs").writeFileSync("HisabDo_AI_Capstone_Day8.docx", buffer);
  console.log("Document created successfully.");
});
