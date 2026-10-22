from fastapi import Header, Request
from pydantic import BaseModel, Field
from sqlalchemy import text

from common.platform import Fault, create_service, idempotent
from services.notification.domain import can_deliver


app, engine = create_service("notification", [
    "CREATE TABLE IF NOT EXISTS deliveries (booking_id TEXT PRIMARY KEY, recipient TEXT NOT NULL, state TEXT NOT NULL)",
])


class Delivery(BaseModel):
    booking_id: str = Field(min_length=1, max_length=128)
    recipient: str = Field(min_length=3, max_length=160)
    simulate_failure: bool = False


@app.post("/api/v1/deliveries", status_code=201)
def deliver(body: Delivery, request: Request, idempotency_key: str = Header(...)):
    def action(connection):
        if not can_deliver(body.simulate_failure):
            raise Fault(503, "PROVIDER_UNAVAILABLE", "Mock notification provider refused delivery")
        connection.execute(text("INSERT INTO deliveries VALUES (:booking_id, :recipient, 'DELIVERED') ON CONFLICT DO NOTHING"), body.model_dump())
        return 201, {"booking_id": body.booking_id, "state": "DELIVERED"}
    return idempotent(engine, request, idempotency_key, body.model_dump(), action)


@app.get("/api/v1/deliveries/{booking_id}")
def get_delivery(booking_id: str):
    with engine.connect() as connection:
        row = connection.execute(text("SELECT * FROM deliveries WHERE booking_id = :id"), {"id": booking_id}).mappings().first()
        if not row:
            raise Fault(404, "NOT_FOUND", "Delivery not found")
        return dict(row)