# Day 8 - Main Capstone Project: AI/ML Use Cases for HisabDo

This folder contains my Day 8 capstone submission for the remote internship —
an analysis of HisabDo (hisabdo.app) identifying practical AI/ML opportunities
across its website, web application, and mobile application.

## 📁 What's in this project

| File | Description |
|---|---|
| `HisabDo_AI_Capstone_Day8.docx` | The main deliverable — full use case document, architecture, and feedback. |
| `build_doc.js` | Script used to generate the Word document (for reference/reproducibility). |

## 📄 Document Contents

1. **Introduction & Objective**
2. **Product Exploration** — HisabDo's personas, existing features, and typical user workflow
3. **5 AI/ML Use Cases**, each with all 7 required fields:
   - Smart Reminders for Overdue Udhar
   - OCR Receipt / Bill Scanner
   - Smart Expense/Transaction Categorization
   - AI Financial Insights (Cash Flow Health Summary)
   - Voice-Based AI Query Assistant
4. **User Feedback** — direct, hands-on feedback from using the app
5. **Top 2 Feature Architecture** (User → Application → AI Service → Model/API → Response):
   - Smart Reminders for Overdue Udhar
   - OCR Receipt / Bill Scanner
6. **Short Implementation Explanation**
7. **Conclusion**

## 🧠 How the Top 2 Features Were Chosen

Selection was based on real, direct user feedback gathered from hands-on use
of the app (Section 4 of the document) — not assumed priorities. "Smart
reminders for overdue udhar" was the explicit most-wanted improvement, and
"no AI/smart help — fully manual entry" was the clearest friction point,
which OCR receipt scanning most directly addresses for the wholesaler/
shopkeeper personas.

**Note on scope:** the task's User Feedback Activity calls for feedback from
five distinct users. This submission includes one direct, hands-on account.
A fuller version of this activity would involve structured feedback from at
least five users across HisabDo's core personas (shopkeeper, freelancer,
wholesaler, home-based seller) to validate these priorities more broadly —
this is noted transparently within the document itself.

## 🛠️ How to Rebuild the Document

```bash
npm install docx
node build_doc.js
```

## 👤 Author
Abbas Raza
- GitHub: [AbbasRaza5055](https://github.com/AbbasRaza5055)

---
*Day 8 task — analyzing a real product (HisabDo) and proposing grounded,
technically-specified AI/ML features rather than generic fintech AI ideas.*
