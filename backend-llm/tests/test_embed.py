# Tests for the embed creation


def test_embed_success(client, monkeypatch):
    """It should return a new embedding"""

    # Fake chat response
    def fake_embedding(model, prompt):
        return {"embedding": [0.1, 0.2, 0.3]}

    monkeypatch.setattr("app.api.v1.embed.ollama.embeddings", fake_embedding)

    # "Call" to the API
    body = {"text": "Maíz"}
    res = client.post("/embed", json=body)

    assert res.status_code == 200
    assert res.json() == {"embedding": [0.1, 0.2, 0.3]}


def test_empty_embed(client, monkeypatch):
    """It should return empty text exception"""

    # "Call" to the API
    body = {"text": ""}
    res = client.post("/embed", json=body)

    assert res.status_code == 422
    assert res.json() == {"detail": "Field text empty."}


def test_embed_error(client, monkeypatch):
    """It should return embed's failure"""

    # Fake embed response
    def fake_embed_error(*args, **kwargs):
        raise RuntimeError("ollama out of service")

    # Replaces the expected function with the fake one.
    monkeypatch.setattr("app.api.v1.embed.ollama.embeddings", fake_embed_error)

    # "Call" to the API
    body = {"text": "Maíz"}
    res = client.post("/embed", json=body)

    assert res.status_code == 500
    assert res.json() == {"detail": "ollama out of service"}
