import pytest
from app.api import router
from app.models import Prompt
from fastapi.testclient import TestClient

# Initialize the TestClient with the FastAPI router
client = TestClient(router)


# Test for listing prompt versions

def test_list_prompt_versions():
    response = client.get("/prompts/test-prompt-id/versions")
    assert response.status_code == 200
    # Expect an empty list initially because no versions have been created
    assert response.json() == []


# Test for reverting to an older version

def test_revert_to_old_version():
    # Revert will fail initially since we haven't implemented it
    response = client.put("/prompts/test-prompt-id/versions/test-version-id/revert")
    assert response.status_code == 404  # Expect this until we implement versioning


# These tests should fail until the versioning system has been implemented, 
# indicating the correct starting point for TDD.
