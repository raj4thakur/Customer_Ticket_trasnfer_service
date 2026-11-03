from fastapi import FastAPI,HTTPException
from app.model_schema import TicketCreate, TicketResponse,TicketPredictRequest, TicketPredictResponse
from app.model_loader import load_artifacts
from app.predictor import predict_ticket
from app.decision_enginer import transfer_to_team
from datetime import datetime, timezone
from app.ticket_storage import (
    add_ticket,
    get_all_tickets,
    get_ticket_by_id
)


artifacts = load_artifacts()

app = FastAPI(title="Customer support Ticketing System")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Customer Support Ticketing System",
            "teams": ['product_team','success_team','engineering','billing_team','compliance_team','auth_team'],
            "urgency_levels": ['low', 'medium', 'high','critical']}

@app.post("/tickets/",response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate):
    try:
        current_time=datetime.now(timezone.utc).isoformat()
        prediction = predict_ticket(
           subject=ticket.subject,
              body=ticket.issue_description,
              artifacts=artifacts)
        new_ticket = {
           "ticket_id": 1,
              "customer_id": ticket.customer_id,
                "channel": ticket.channel,
                "subject": ticket.subject,
                "issue_description": ticket.issue_description,
                "priority": prediction["urgency"],
                "customer_tier": "standard",
                "resolution_status": "open",
                "created_at": current_time,
                "updated_at": current_time,
                "language": "en",
                "category": prediction["category"],
                "urgency": prediction["urgency"],
                "assigned_team": transfer_to_team(prediction["category"])}
        saved_ticket = add_ticket(new_ticket)
        return saved_ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ticket creation failed: {str(e)}")

    
@app.get("/tickets/",response_model=list[TicketResponse])
async def list_tickets():
    try:
        tickets = get_all_tickets()
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tickets: {str(e)}")

@app.get("/tickets/{ticket_id}",response_model=TicketResponse)
async def get_ticket(ticket_id: int):
    try:
        ticket = get_ticket_by_id(ticket_id)
        if ticket is None:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve ticket: {str(e)}")