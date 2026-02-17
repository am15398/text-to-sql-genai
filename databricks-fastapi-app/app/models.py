from pydantic import BaseModel

class Claim(BaseModel):
    claim_id: str
    member_id: str
    amount: float