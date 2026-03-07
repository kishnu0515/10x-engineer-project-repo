import pytest
from pydantic import ValidationError
from datetime import datetime

# Support both import paths depending on runner config
try:
    from backend.app.models import (
        Prompt,
        PromptCreate,
        PromptUpdate,
        PromptPartialUpdate,
        Collection,
        CollectionCreate,
        PromptList,
        CollectionList,
        HealthResponse,
    )
except ModuleNotFoundError:  # pragma: no cover - fallback for alternate envs
    from app.models import (
        Prompt,
        PromptCreate,
        PromptUpdate,
        PromptPartialUpdate,
        Collection,
        CollectionCreate,
        PromptList,
        CollectionList,
        HealthResponse,
    )


# =============================
# Model validation
# =============================

def test_prompt_model_validation():
    # Empty title and content should fail min_length
    with pytest.raises(ValidationError):
        Prompt(title="", content="")

    # Valid
    valid_prompt = Prompt(title="Example", content="Sample content")
    assert valid_prompt.title == "Example"


def test_prompt_update_validation():
    # PromptUpdate requires all fields (inherits PromptBase)
    data = {"title": "T", "content": "C", "description": "D", "collection_id": None}
    pu = PromptUpdate(**data)
    assert pu.title == "T"

    # Missing content should fail
    with pytest.raises(ValidationError):
        PromptUpdate(title="Only title")  # type: ignore[arg-type]


def test_prompt_partial_update_validation():
    # Partial update accepts any subset and validates constraints
    ppu = PromptPartialUpdate(title="New Title")
    assert ppu.title == "New Title"
    # Empty title should fail min_length
    with pytest.raises(ValidationError):
        PromptPartialUpdate(title="")


# =============================
# Default values
# =============================

def test_prompt_default_values_and_types():
    p = Prompt(title="A", content="B")
    assert isinstance(p.id, str) and len(p.id) == 36
    assert isinstance(p.created_at, datetime)
    assert isinstance(p.updated_at, datetime)
    assert p.description is None
    assert p.collection_id is None


def test_collection_default_values_and_types():
    c = Collection(name="Example Collection")
    assert isinstance(c.id, str) and len(c.id) == 36
    assert isinstance(c.created_at, datetime)
    assert isinstance(c.prompts, list) and c.prompts == []


def test_collection_prompts_list_is_independent():
    c1 = Collection(name="One")
    c2 = Collection(name="Two")
    c1.prompts.append("p1")
    assert c1.prompts == ["p1"]
    assert c2.prompts == []  # default_factory ensures different list objects


# =============================
# Serialization
# =============================

def test_prompt_serialization_to_json():
    p = Prompt(title="Ser", content="X")
    # Pydantic v2: mode="json" converts datetimes to ISO strings
    dumped = p.model_dump(mode="json")
    assert isinstance(dumped["created_at"], str)
    assert isinstance(dumped["updated_at"], str)
    # Ensure id/title/content present
    assert dumped["id"] == p.id
    assert dumped["title"] == "Ser"


def test_collection_serialization_to_json():
    c = Collection(name="C")
    dumped = c.model_dump(mode="json")
    assert isinstance(dumped["created_at"], str)
    assert dumped["prompts"] == []


def test_response_models_serialization():
    p = Prompt(title="R", content="Q")
    pl = PromptList(prompts=[p], total=1)
    d = pl.model_dump(mode="json")
    assert d["total"] == 1
    assert isinstance(d["prompts"][0]["created_at"], str)

    c = Collection(name="CC")
    cl = CollectionList(collections=[c], total=1)
    d2 = cl.model_dump(mode="json")
    assert d2["total"] == 1
    assert isinstance(d2["collections"][0]["created_at"], str)


def test_health_response_serialization():
    h = HealthResponse(status="healthy", version="1.0.0")
    d = h.model_dump()
    assert d == {"status": "healthy", "version": "1.0.0"}