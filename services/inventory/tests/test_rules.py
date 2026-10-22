from concurrent.futures import ThreadPoolExecutor
import os
import uuid

import pytest
from sqlalchemy import create_engine, text

from services.inventory.domain import RuleViolation, release, reserve


@pytest.fixture
def engine():
    database = create_engine(os.environ["TEST_DATABASE_URL"], pool_size=25)
    with database.begin() as connection:
        connection.execute(text("CREATE TABLE IF NOT EXISTS released_holds (id TEXT PRIMARY KEY)"))
        connection.execute(text("CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, name TEXT NOT NULL, capacity INTEGER NOT NULL, available INTEGER NOT NULL CHECK (available >= 0 AND available <= capacity), price_cents INTEGER NOT NULL)"))
        connection.execute(text("CREATE TABLE IF NOT EXISTS holds (id TEXT PRIMARY KEY, event_id TEXT NOT NULL REFERENCES events(id), quantity INTEGER NOT NULL, state TEXT NOT NULL)"))
    yield database
    database.dispose()


def test_br1_twenty_requests_cannot_overallocate(engine):
    event_id = str(uuid.uuid4())
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO events VALUES (:id, 'Test', 5, 5, 2500)"), {"id": event_id})

    def attempt(index):
        try:
            with engine.begin() as connection:
                reserve(connection, event_id, 1, f"{event_id}-{index}")
            return True
        except RuleViolation:
            return False

    with ThreadPoolExecutor(max_workers=20) as pool:
        results = list(pool.map(attempt, range(20)))
    assert sum(results) == 5
    with engine.connect() as connection:
        assert connection.execute(text("SELECT available FROM events WHERE id = :id"), {"id": event_id}).scalar_one() == 0


def test_br2_release_is_idempotent(engine):
    event_id = str(uuid.uuid4())
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO events VALUES (:id, 'Test', 1, 1, 2500)"), {"id": event_id})
        reserve(connection, event_id, 1, event_id)
        release(connection, event_id)
        release(connection, event_id)
        assert connection.execute(text("SELECT available FROM events WHERE id = :id"), {"id": event_id}).scalar_one() == 1


def test_br2_release_before_late_reservation_prevents_leak(engine):
    reservation_id = str(uuid.uuid4())
    with engine.begin() as connection:
        release(connection, reservation_id)
        with pytest.raises(RuleViolation, match="already cancelled"):
            reserve(connection, "late-event", 1, reservation_id)