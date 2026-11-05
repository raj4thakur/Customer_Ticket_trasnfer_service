
from datetime import datetime

from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    channel: str = "email"
    subject: str = Field(..., min_length=1)
    issue_description: str = Field(..., min_length=5)


class TicketResponse(BaseModel):
    channel: str
    subject: str
    issue_description: str
    customer_tier: str
    resolution_status: str
    created_at: datetime
    updated_at: datetime
    language: str
    category: str
    urgency: str
    assigned_team:str
