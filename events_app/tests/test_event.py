import falcon

EVENT_ID = "32ca3481-b44a-4832-ad98-8bfdd00dc8e3"
USER_ID = "93db8fcb-319d-4867-9f18-dec3ee5a2f9b"


def test_ping(client):
    result = client.simulate_get('/')
    assert result.status == falcon.HTTP_200
    assert result.json == "Ping"


def test_create_event(client):
    event = {"user_id": USER_ID, "title": "test title", "description": "test description"}
    result = client.simulate_post('/event', json=event)
    assert result.status == falcon.HTTP_201
    assert result.json.get("event_id") is not None


def test_get_event_by_id(client):
    result = client.simulate_get('/event', params={"event_id": EVENT_ID})
    assert result.status == falcon.HTTP_200
    assert list(result.json[0].keys()) == ['description', 'event_id', 'meta_create_ts', 'meta_update_ts',
                                           'title', 'ts_description', 'ts_title', 'user_id']


def test_get_user_events(client):
    result = client.simulate_get('/event', params={"user_id": USER_ID})
    assert result.status == falcon.HTTP_200
    assert list(result.json[0].keys()) == ['description', 'event_id', 'meta_create_ts',
                                           'meta_update_ts', 'title', 'ts_description', 'ts_title', 'user_id']


def test_delete_event(client):
    result = client.simulate_delete('/event', params={"event_id": EVENT_ID})
    assert result.status == falcon.HTTP_200
    assert result.json == {"message": "deleted"}


