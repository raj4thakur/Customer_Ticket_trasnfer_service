from fastapi import FastAPI,HTTPException
from app.model_schema import TicketCreate, TicketResponse
from app.model_loader import load_artifacts
from app.predictor import predict_ticket
from app.decision_enginer import transfer_to_team
from datetime import datetime, timezone
from app.ticket_storage import add_ticket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

artifacts = load_artifacts()

app = FastAPI(title="Customer support Ticketing System")

BASE_DIR = Path(__file__).resolve().parent.parent

app.mount(
    "/templates",
    StaticFiles(directory=BASE_DIR / "templates"),
    name="templates"
)


@app.get("/", include_in_schema=False)
async def ticket_ui():
    return FileResponse(BASE_DIR / "templates" / "ticket.html")

@app.post("/tickets/",response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate):
    try:
        current_time=datetime.now(timezone.utc).isoformat()
        prediction = predict_ticket(
           subject=ticket.subject,
              body=ticket.issue_description,
              artifacts=artifacts)
        print(f"catergory:{prediction['category']}, Confidence:{prediction['category_confidence']}")
        print(f"Urgency:{prediction['urgency']}, Confidence:{prediction['urgency_confidence']}")
        new_ticket = {
                "channel": ticket.channel,
                "subject": ticket.subject,
                "issue_description": ticket.issue_description,
                "urgency": prediction["urgency"],
                "customer_tier": "standard",
                "resolution_status": "open",
                "created_at": current_time,
                "updated_at": current_time,
                "language": "en",
                "category": prediction["category"],
                "assigned_team": transfer_to_team(prediction["category"])}
        saved_ticket = add_ticket(new_ticket)
        return saved_ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ticket creation failed: {str(e)}")