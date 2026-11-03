import json
import threading
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TICKETS_FILE = DATA_DIR / "tickets.json"

# Prevent simultaneous requests from writing to the file at the same time.
_file_lock = threading.Lock()


def load_tickets():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not TICKETS_FILE.exists():
        save_tickets([])

    with open(TICKETS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_tickets(tickets):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    temp_file = TICKETS_FILE.with_suffix(".tmp")

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4, ensure_ascii=False)

    temp_file.replace(TICKETS_FILE)


def get_next_ticket_id(tickets):
    if not tickets:
        return 1001

    return max(ticket["ticket_id"] for ticket in tickets) + 1


def add_ticket(ticket):
    with _file_lock:
        tickets = load_tickets()

        ticket["ticket_id"] = get_next_ticket_id(tickets)

        tickets.append(ticket)
        save_tickets(tickets)

        return ticket


def get_all_tickets():
    with _file_lock:
        return load_tickets()


def get_ticket_by_id(ticket_id):
    with _file_lock:
        tickets = load_tickets()

        for ticket in tickets:
            if ticket["ticket_id"] == ticket_id:
                return ticket

    return None