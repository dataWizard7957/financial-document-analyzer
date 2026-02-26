# Financial Document Analyzer API

A FastAPI-based service to extract structured insights from financial documents (PDFs) using AI agents via CrewAI and Groq LLM (LLaMA3).

## Table of Contents

Project Overview

Issues Found and Fixes

Setup Instructions

Usage Instructions

API Documentation

Example Output

## Project Overview

This API allows users to upload financial PDFs and query them for key metrics, performance summaries, and risk assessment. The API ensures that outputs are returned in strict JSON format for consistency.

## Tech Stack

Backend Framework: FastAPI

AI Agents: CrewAI (v0.130.0)

Language Model: Groq LLaMA3-8B

Document Loader: LangChain Community PyPDFLoader

Environment & Dependencies: Python, Pydantic v2, Uvicorn

## Key features:

Extract company name, reporting period, and financial metrics (revenue, net income, EPS, etc.)

Summarize performance and identify risk factors

Assess risk level with justification

Handles multiple-page PDFs (truncated to prevent token overflow)

Uses CrewAI Agent + Task framework for structured LLM execution

## Issues Found and Fixes
Deterministic Bugs

1️⃣ Undefined / Improper LLM Initialization
Problem: LLM instance was undefined or misconfigured, causing runtime errors.
Fix: Created a proper Groq LLM instance with the model set, deterministic temperature, and a max token limit to ensure stable execution.

2️⃣ PDF Loader Not Imported / Incorrect
Problem: Original code used an undefined PDF class or loader.
Fix: Replaced with the correct PDF loader to properly read uploaded files.

3️⃣ Uploaded File Not Passed
Problem: The uploaded PDF path was never passed into Crew or agent.
Fix: Ensured the file path is provided to the agent during task execution.

4️⃣ Async Tool Misuse
Problem: Tools were declared asynchronous but not awaited properly, causing execution errors.
Fix: Converted tools to synchronous functions for stable execution.

5️⃣ No Context Size Control (Crash Risk)
Problem: Entire PDFs were loaded without limits, risking token overflow.
Fix: Added limits: maximum 5 pages and maximum 10,000 characters per PDF.

6️⃣ Delegation Enabled Unnecessarily
Problem: Delegation settings increased token usage and unpredictable results.
Fix: Disabled delegation to enforce deterministic behavior.

7️⃣ Memory and Verbose Mode Enabled
Problem: Memory and verbose settings caused unnecessary token growth.
Fix: Disabled both to ensure clean, isolated execution per request.

8️⃣ LLM Provider Not Specified
Problem: Missing LLM provider caused API errors when initializing the model.
Fix: Explicitly specified the LLM provider with API key and model configuration.

9️⃣ Task / Agent Execution Errors
Problem: Creating tasks dynamically using copy methods caused missing argument errors.
Fix: Created a new task instance for each request instead of copying.

🔟 Module / Import Errors
Problem: Missing or unnecessary imports caused module not found errors.
Fix: Removed invalid imports; tasks now use valid CrewAI Agent objects.

1️⃣1️⃣ Pydantic Field Errors
Problem: Non-annotated fields caused validation errors.
Fix: Properly annotated all Task and Agent fields to comply with Pydantic v2.

1️⃣2️⃣ Abstract Method Instantiation Error
Problem: Custom tools without implemented _run methods caused type errors.
Fix: Removed abstract tool implementations; tasks now directly use agents.

Inefficient / Unsafe Prompts

1️⃣ Non-JSON or Verbose Responses Allowed
Problem: Prompts allowed non-structured or overly verbose outputs.
Fix: Rewrote task instructions to enforce strict JSON output for consistent results.

2️⃣ Unbounded / Unsafe Creativity
Problem: Prompts allowed hallucination, making up investment advice, or ignoring user queries.
Fix: Strictly tied analysis to document content; fabrication removed.

3️⃣ Fake URLs / Unsafe Recommendations
Problem: Prompts instructed including fake financial websites or recommending extreme investments.
Fix: Removed entirely; analysis is neutral and evidence-based.

4️⃣ Contradictions Allowed
Problem: Prompts allowed contradictory analysis.
Fix: Enforced a structured JSON schema for consistent and reliable outputs.

5️⃣ Limited PDF / Context Control Missing
Problem: Prompts did not enforce page or character limits, risking token overflow.
Fix: Added maximum pages and character limits to prevent truncation or crashes.

## Setup Instructions

1️⃣ Clone the repository

git clone <repo_url>
cd <repo_directory>

2️⃣ Create virtual environment

python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Set environment variables

Create a .env file:

GROQ_API_KEY=<your_groq_api_key>

## Usage Instructions

1️⃣ Run the API

uvicorn main:app --reload

2️⃣ Open in browser

Visit: http://127.0.0.1:8000/

You should see:

{"message": "Financial Document Analyzer API is running"}

3️⃣ Upload PDF and query

Endpoint: POST /analyze

Form data:

file: PDF file

query: Query string, e.g., "List company name, reporting period, and key metrics"

API Documentation

GET /

Description: Health check endpoint

Response:

{
  "message": "Financial Document Analyzer API is running"
}

POST /analyze

Description: Analyze a financial PDF and return structured JSON output

Request: multipart/form-data

Field	Type	Description
file	PDF	The financial document to analyze
query	str	User query to extract specific data

Response: 200 OK

## Example JSON output:

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
      "performance_summary": "Tesla's Q2 2025 update highlights the company's transition to AI, robotics...",
      "risk_factors": [
        "Uncertain macroeconomic environment",
        "Shifting tariffs",
        "Changes to fiscal policy and political sentiment"
      ]
    },
    "risk_assessment": {
      "risk_level": "Medium",
      "justification": "The company's transition to new markets and services..."
    },
    "limitations": "The analysis is based on the provided financial document..."
  }
}

Error Responses:

Code	Message
400	Invalid file type / text extraction failed
500	LLM call failed or internal server error

Notes

Only PDF files are supported.

The response JSON is strictly structured for grading or downstream automation.

The API truncates long PDFs to prevent token overflow (MAX_PAGES=5, MAX_CHARACTERS=5000).
