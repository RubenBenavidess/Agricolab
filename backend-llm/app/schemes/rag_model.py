# Schema for the rag.
from pydantic import BaseModel

class RagRequest(BaseModel):
    question: str
    n_docs: int = 4                  # Modify depending on how many documents the model will process


class RagResponse(BaseModel):
    answer: str
    sources: list[str]
    