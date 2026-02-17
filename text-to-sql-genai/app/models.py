from pydantic import BaseModel

class PromptRequest(BaseModel):
    question: str
