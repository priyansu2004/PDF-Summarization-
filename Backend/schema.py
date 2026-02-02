from pydantic import BaseModel


class responseText(BaseModel):
    text: str

class requestText(BaseModel):
    text: str
    