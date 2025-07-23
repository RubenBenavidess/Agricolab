# Tests for the chat


def test_chat_success(client, monkeypatch):
    """It should return ollama's response"""

    # Fake chat response
    def fake_chat(model, messages, stream=False):
        prompt = messages[0]["content"]
        return {"message": {"content": f"ECHO: {prompt}"}}

    # Replaces the expected function with the fake one.
    monkeypatch.setattr("app.api.v1.chat.ollama.chat", fake_chat)

    # "Call" to the API
    body = {"prompt": "hi", "stream": False}
    res = client.post("/chat", json=body)

    assert res.status_code == 200
    assert res.json() == {"response": "ECHO: hi"}


def test_chat_error(client, monkeypatch):
    """It should return ollama's failure"""

    # Fake chat response
    def fake_chat_error(*args, **kwargs):
        raise RuntimeError("ollama out of service")

    # Replaces the expected function with the fake one.
    monkeypatch.setattr("app.api.v1.chat.ollama.chat", fake_chat_error)

    # "Call" to the API
    res = client.post("/chat", json={"prompt": "hola"})
    assert res.status_code == 500
    assert res.json() == {"detail": "ollama out of service"}
