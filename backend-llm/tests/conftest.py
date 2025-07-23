import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def client():
    # It allows to test API requests without the API execution
    return TestClient(app)
