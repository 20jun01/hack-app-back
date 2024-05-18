from pydantic import BaseModel


class ChatGPTResponse(BaseModel):
    category: str
    subcategory: str
    summary: str
    title: str
