import pytest
from fastapi.testclient import TestClient
from app.api import router

# Initialize the TestClient with the FastAPI router
client = TestClient(router)

# Example test cases - expand these based on your API endpoints

def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}


def test_list_prompts_success():
    response = client.get("/prompts")
    assert response.status_code == 200
    # Further assertions based on expected output


def test_get_prompt_not_found():
    response = client.get("/prompts/non-existing-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Prompt not found"}

# More tests to be added to cover happy paths, error cases, and edge cases.