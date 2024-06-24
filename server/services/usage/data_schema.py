from typing import List, Optional
from pydantic import BaseModel


class MessageItem(BaseModel):
    text: str
    timestamp: str
    report_id: Optional[int] = None
    id: int


class MessagesResponse(BaseModel):
    messages: List[MessageItem]


class ReportItem(BaseModel):
    id: int
    name: str
    credit_cost: float


class UsageItem(BaseModel):
    message_id: int
    timestamp: str
    report_name: Optional[str]
    credits_used: float


class UsageData(BaseModel):
    usage: List[UsageItem]
