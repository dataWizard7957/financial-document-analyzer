# main.py

import os
import io
import json
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pdfplumber

from crewai import Agent, Task, Crew, Process
from task import analyze_financial_document

# Load environment variables
load_dotenv()

app = FastAPI(title="Financial Document Analyzer API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_PAGES = 5
MAX_CHARACTERS = 5000

@app.get("/")
def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    query: str = Form(...)
):
    try:
        # Validate file type
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

        # Read PDF
        pdf_bytes = await file.read()
        text = ""

        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            total_pages = min(len(pdf.pages), MAX_PAGES)
            for i in range(total_pages):
                page = pdf.pages[i]
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

        # Limit characters
        text = text[:MAX_CHARACTERS]

        # Update Task description dynamically with document + query
        analyze_financial_document.description = f"""
Analyze the following financial document and answer the user's query.

Document:
{text}

User Query:
{query}

Return the response strictly in valid JSON format.
"""
        
        # Execute Task via Crew
        crew = Crew(
            agents=[analyze_financial_document.agent],
            tasks=[analyze_financial_document],
            process=Process.sequential,
            verbose=False
        )
        result = crew.kickoff()

        # Parse raw string into JSON
        raw_result = result.raw if hasattr(result, "raw") else result.get("raw", "")
        try:
            json_result = json.loads(raw_result)
        except Exception:
            json_result = raw_result  # fallback if parsing fails

        return {"result": json_result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
