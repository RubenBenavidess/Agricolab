# Test for the base route.
def test_health(client):
    """It should return status: ok"""
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
