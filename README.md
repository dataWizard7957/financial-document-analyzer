# 📊 Financial Document Analyzer API

A FastAPI service for extracting structured insights from financial PDF documents using AI agents powered by CrewAI and Groq LLaMA3.

---

## 🚀 Overview

Upload financial PDFs and query them for key insights such as financial metrics, performance summaries, and risk assessments.
All responses are returned in a strict JSON format for consistency and easy integration.

---

## 🏗️ Tech Stack

* **Backend:** FastAPI
* **AI Orchestration:** CrewAI (v0.130.0)
* **LLM:** Groq LLaMA3-8B
* **Document Processing:** LangChain PyPDFLoader
* **Environment:** Python, Pydantic v2, Uvicorn

---

## ✨ Features

* Extracts:

  * Company name, reporting period
  * Key financial metrics (revenue, net income, EPS, etc.)
* Performance summarization and risk identification
* Structured risk assessment with justification
* Multi-page PDF support with controlled truncation
* Deterministic, schema-driven JSON outputs
* Modular AI pipeline using agents and tasks

---

## ⚙️ Setup

```bash
git clone <repo_url>
cd <repo_directory>
pip install -r requirements.txt
```

Create `.env`:

```env
GROQ_API_KEY=<your_groq_api_key>
```

Run:

```bash
uvicorn main:app --reload
```

---

## ▶️ Usage

* **Health Check:** `GET /`
* **Analyze Document:** `POST /analyze`

**Request (multipart/form-data):**

* `file`: PDF document
* `query`: e.g., *"List company name, reporting period, and key metrics"*

---

## 📊 Response (Example)

```json
{
  "result": {
    "validation": {
      "valid": true,
      "document_type": "Q2 2025 Update",
      "confidence": "High"
    },
    "analysis": {
      "company_name": "Tesla",
      "reporting_period": "Q2 2025",
      "key_metrics": {
        "revenue": "$22,496 million",
        "net_income": "$1.2B GAAP net income, $1.4B non-GAAP net income",
        "operating_income": "$923 million",
        "eps": "$0.33 GAAP EPS, $0.40 non-GAAP EPS",
        "total_assets": "$36.8B",
        "total_liabilities": "Not specified"
      },
      "performance_summary": "Tesla's Q2 2025 update highlights the company's transition to AI and robotics...",
      "risk_factors": [
        "Uncertain macroeconomic environment",
        "Shifting tariffs",
        "Changes to fiscal policy and political sentiment"
      ]
    },
    "risk_assessment": {
      "risk_level": "Medium",
      "justification": "The company's transition to new markets and services introduces moderate uncertainty..."
    },
    "limitations": "The analysis is based solely on the provided financial document."
  }
}
```

---

## ⚠️ Errors

* **400:** Invalid file or extraction failure
* **500:** LLM or internal processing error

---

## 📌 Notes

* Only PDF files are supported
* Strict JSON response schema
* Input limits:

  * `MAX_PAGES = 5`
  * `MAX_CHARACTERS = 5000`
