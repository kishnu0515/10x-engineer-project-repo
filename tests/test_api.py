import pytest
from fastapi.testclient import TestClient
from backend.app.api import router
# Import necessary models for creating test data
from backend.app.models import PromptCreate

# Initialize the TestClient with the FastAPI router
client = TestClient(router)

# =============================
# Health Check Tests
# =============================
def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}

# =============================
# List Prompts Tests
# =============================

def test_list_prompts_success():
    response = client.get("/prompts")
    assert response.status_code == 200
    # Further assertions based on expected output

def test_get_prompt_not_found():
    response = client.get("/prompts/non-existing-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Prompt not found"}

# =============================
# Happy Path Tests
# =============================

def test_create_prompt_success():
    new_prompt = {
        "title": "Test Prompt",
        "content": "This is a test content.",
        "description": "A test prompt description",
    }
    response = client.post("/prompts", json=new_prompt)
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["title"] == new_prompt["title"]
    assert json_response["content"] == new_prompt["content"]

# =============================
# Error Case Tests
# =============================

def test_create_prompt_invalid_data():
    incomplete_prompt = {
        "title": 123,  # Invalid type, should be a string
        "content": "Test content missing title",
    }
    response = client.post("/prompts", json=incomplete_prompt)
    assert response.status_code == 400  # Expecting a validation error

# =============================
# Edge Case Tests
# =============================

def test_create_prompt_empty_title():
    empty_title_prompt = {
        "title": "",  # Edge case: empty title
        "content": "This content has no title.",
        "description": "Edge case with empty title",
    }
    response = client.post("/prompts", json=empty_title_prompt)
    assert response.status_code == 400  # Validation should fail for empty title

# More tests to be added to cover happy paths, error cases, and edge cases.