
from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    customer_id: int = Field(..., gt=0)
    channel: str = "email"
    subject: str = Field(..., min_length=1)
    issue_description: str = Field(..., min_length=5)


class TicketResponse(BaseModel):
    ticket_id: int
    customer_id: int
    channel: str
    subject: str
    issue_description: str
    customer_tier: str
    resolution_status: str
    created_at: str
    updated_at: str
    language: str
    category: str
    urgency: str
    assigned_team:str
