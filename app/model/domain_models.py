from pydantic import BaseModel
class ChatGPTResponse(BaseModel):
    answer: str
