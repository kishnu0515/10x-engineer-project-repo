import pytest
from pydantic import ValidationError
from backend.app.models import Prompt, Collection, Tag  # Adjusted imports to reflect the correct module path
# Example model validation tests

def test_prompt_model_validation():
    with pytest.raises(ValidationError):
        Prompt(title="", content="")  # Title and Content validation

    valid_prompt = Prompt(title="Example", content="Sample content")
    assert valid_prompt.title == "Example"


def test_collection_default_values():
    collection = Collection(name="Example Collection")
    assert collection.prompts == []

# More tests to validate default values, serialization, and error conditions.