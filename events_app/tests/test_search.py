import falcon

USER_ID = "93db8fcb-319d-4867-9f18-dec3ee5a2f9b"


def test_search_title(client):
    result = client.simulate_get('/search', params={"user_id": USER_ID, "query": "title", "type": "title"})
    assert result.status == falcon.HTTP_200
    assert list(result.json[0].keys()) == ['description', 'event_id', 'similarity', 'title', 'ts_rank']


def test_search_description(client):
    result = client.simulate_get('/search', params={"user_id": USER_ID, "query": "description", "type": "description"})
    assert result.status == falcon.HTTP_200
    assert list(result.json[0].keys()) == ['description', 'event_id', 'similarity', 'title', 'ts_rank']
    print(list(result.json[0].keys()))


def test_search_title_description(client):
    result = client.simulate_get('/search', params={"user_id": USER_ID, "query": "test",
                                                    "description": "description 1", "type": "both"})
    assert result.status == falcon.HTTP_200
    print(list(result.json[0].keys()))
    assert list(result.json[0].keys()) == ['description', 'event_id', 'similarity', 'title', 'ts_rank']



