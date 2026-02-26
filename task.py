# task.py

from crewai import Task
from agents import financial_analyst

analyze_financial_document = Task(
    description="""
Analyze the provided financial document content.

Steps:
1. Determine if the document is financial in nature.
2. Extract:
   - Company name
   - Reporting period
   - Revenue
   - Net income
   - Operating income
   - EPS
   - Total assets
   - Total liabilities
3. Summarize performance.
4. Identify risk factors mentioned in the document.
5. Classify overall risk level (Low, Moderate, High).

Rules:
- Use only provided document content.
- Do not fabricate information.
- If data is missing, state "Information not available in document."
- Do not provide investment advice.
- Return STRICT JSON only.
""",
    expected_output="""
Return STRICT JSON:

{
  "validation": {
    "valid": true,
    "document_type": "",
    "confidence": ""
  },
  "analysis": {
    "company_name": "",
    "reporting_period": "",
    "key_metrics": {
      "revenue": "",
      "net_income": "",
      "operating_income": "",
      "eps": "",
      "total_assets": "",
      "total_liabilities": ""
    },
    "performance_summary": "",
    "risk_factors": []
  },
  "risk_assessment": {
    "risk_level": "",
    "justification": ""
  },
  "limitations": ""
}
""",
    agent=financial_analyst,
    async_execution=False,
)
