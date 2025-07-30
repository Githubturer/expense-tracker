from pydantic import BaseModel

class EmailVerification(BaseModel):
    subject: str
    body: str
    to: list[str]
