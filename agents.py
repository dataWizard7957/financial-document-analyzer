# agents.py

import os
from dotenv import load_dotenv

from crewai import Agent, LLM

# Load environment variables
load_dotenv()

# Validate Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# LLM Configuration (Groq - Llama 3.1 8B Instant)
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    temperature=0,          # Deterministic output
    max_tokens=800,         # Safe limit for JSON response
    api_key=GROQ_API_KEY
)

# Financial Analyst Agent
financial_analyst = Agent(
    role="Financial Document Analyst",
    goal="Analyze financial documents and provide structured, fact-based insights.",
    backstory=(
        "You are a professional financial analyst specialized in corporate earnings reports, "
        "quarterly filings, and financial statement interpretation. "
        "You provide objective, compliance-safe, data-driven insights without speculation."
    ),
    verbose=False,
    memory=False,
    allow_delegation=False,
    llm=llm
)
