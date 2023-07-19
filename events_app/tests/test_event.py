import json
import falcon
from falcon import testing
import pytest

import app



@pytest.fixture()
def client():
    """Create falcon testing client to send requests"""
    return testing.TestClient(app.api)


def test_ping(client):
    result = client.simulate_get('/')
    assert result.status == falcon.HTTP_200
    assert result.json == "Ping"


def test_create_event(client):
    event = {"user_id": "93db8fcb-319d-4867-9f18-dec3ee5a2f9b", "title": "test title", "description": "test description"}
    result = client.simulate_post('/event', json=event)
    assert result.status == falcon.HTTP_201
    assert result.json.get("event_id") is not None


def test_get_event_by_id(client):
    result = client.simulate_get('/event', params={"event_id": '32ca3481-b44a-4832-ad98-8bfdd00dc8e3'})
    print(result.json)
    assert result.status == falcon.HTTP_200
    # assert result.json == "Ping"
