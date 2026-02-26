# tools.py

import os
from langchain_community.document_loaders import PyPDFLoader

MAX_PAGES = 5
MAX_CHARACTERS = 10000


class FinancialDocumentTool:
    @staticmethod
    def read_data_tool(path: str) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError("Document not found")

        loader = PyPDFLoader(path)
        pages = loader.load()

        full_text = ""

        for i, page in enumerate(pages):
            if i >= MAX_PAGES:
                break
            full_text += page.page_content.strip() + "\n"

        if len(full_text) > MAX_CHARACTERS:
            full_text = full_text[:MAX_CHARACTERS]

        return full_text
