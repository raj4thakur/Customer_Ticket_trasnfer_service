import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "Raj@Emaster"
}

def add_ticket(ticket: dict):
    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = """
        INSERT INTO tickets (
            subject,
            body,
            channel,
            customer_tier,
            created_at,
            category,
            urgency,
            assigned_team,
            language,
            resolution_status
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        RETURNING *;
        """

        cursor.execute(
            query,
            (
                ticket["subject"],
                ticket["issue_description"],
                ticket["channel"],
                ticket["customer_tier"],
                ticket["created_at"],
                ticket["category"],
                ticket["urgency"],
                ticket["assigned_team"],
                ticket["language"],
                ticket["resolution_status"]
            )
        )

        saved_ticket = cursor.fetchone()

        conn.commit()

        result = dict(saved_ticket)
        # The database column is named ``body`` while the API uses
        # ``issue_description``.
        result["issue_description"] = result.pop("body", ticket["issue_description"])
        # Some existing table definitions do not have an ``updated_at``
        # column. Keep the API response complete using the creation time.
        if result.get("updated_at") is None:
            result["updated_at"] = ticket["updated_at"]
        return result

    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
