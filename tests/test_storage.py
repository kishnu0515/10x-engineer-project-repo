import pytest
from app.storage import Storage
from app.models import Prompt, Collection

# Initialize a Storage object, this might be a mock or a real instance depending on the testing strategy
storage = Storage()

# Example test cases for storage - expand these for comprehensive coverage

def test_create_prompt():
    prompt_data = {"title": "Test Prompt", "content": "Test Content"}
    prompt = Prompt(**prompt_data)
    created_prompt = storage.create_prompt(prompt)
    assert created_prompt.title == prompt_data["title"]
    assert created_prompt.content == prompt_data["content"]


def test_delete_prompt():
    prompt_id = "existing-id"
    assert storage.delete_prompt(prompt_id) is None
    with pytest.raises(Exception):
        storage.get_prompt(prompt_id)

# Add further tests for CRUD operations and edge cases.

import time
from app.models import PromptUpdate, PromptPartialUpdate


@pytest.fixture
def new_storage():
    return Storage()


def test_prompt_crud_operations(new_storage: Storage):
    # Create
    prompt = Prompt(title="Title A", content="Content A")
    created = new_storage.create_prompt(prompt)
    assert created.id == prompt.id
    assert created.title == "Title A"

    # Read
    fetched = new_storage.get_prompt(created.id)
    assert fetched == created

    # Update (full)
    time.sleep(0.01)
    updated = new_storage.update_prompt(
        created.id,
        PromptUpdate(title="New Title", content="New content", description="Desc", collection_id="col-1"),
    )
    assert updated is not None
    assert updated.title == "New Title"
    assert updated.description == "Desc"
    assert updated.collection_id == "col-1"
    assert updated.updated_at >= created.updated_at

    # Partial update
    time.sleep(0.01)
    patched = new_storage.partial_update_prompt(created.id, PromptPartialUpdate(description="Newer desc"))
    assert patched is not None
    assert patched.description == "Newer desc"
    assert patched.updated_at >= updated.updated_at

    # Delete
    assert new_storage.delete_prompt(created.id) is None
    with pytest.raises(KeyError):
        new_storage.get_prompt(created.id)


def test_get_prompts_filter_and_sort(new_storage: Storage):
    p1 = new_storage.create_prompt(Prompt(title="Alpha", content="one"))
    time.sleep(0.01)
    p2 = new_storage.create_prompt(Prompt(title="Beta", content="two", collection_id="C1"))
    time.sleep(0.01)
    p3 = new_storage.create_prompt(Prompt(title="alphabet soup", content="three", collection_id="C1"))

    # Sorted by updated_at desc: p3, p2, p1
    results = new_storage.get_prompts()
    assert [r.id for r in results] == [p3.id, p2.id, p1.id]

    # Search filter is case-insensitive and trimmed
    results = new_storage.get_prompts(search="  AlPhA  ")
    assert set(r.id for r in results) == {p1.id, p3.id}

    # Collection filter
    results = new_storage.get_prompts(collection_id="C1")
    assert [r.id for r in results] == [p3.id, p2.id]


def test_partial_update_no_fields_returns_existing(new_storage: Storage):
    p = new_storage.create_prompt(Prompt(title="T", content="C"))
    old_updated_at = p.updated_at
    same = new_storage.partial_update_prompt(p.id, PromptPartialUpdate())
    assert same is not None
    assert same.updated_at == old_updated_at


def test_update_nonexistent_returns_none(new_storage: Storage):
    assert new_storage.update_prompt("missing", PromptUpdate(title="x", content="y")) is None


def test_delete_collection_nullifies_prompt_collection(new_storage: Storage):
    col = new_storage.create_collection(Collection(name="Dev"))
    p = new_storage.create_prompt(Prompt(title="T", content="C", collection_id=col.id))

    assert new_storage.delete_collection(col.id) is True

    remaining = new_storage.get_prompt(p.id)
    assert remaining is not None
    assert remaining.collection_id is None

    # Deleting a non-existent collection returns False
    assert new_storage.delete_collection("does-not-exist") is False


def test_get_collections_sorted(new_storage: Storage):
    c1 = new_storage.create_collection(Collection(name="A"))
    time.sleep(0.01)
    c2 = new_storage.create_collection(Collection(name="B"))
    res = new_storage.get_collections()
    assert [c.id for c in res] == [c2.id, c1.id]


def test_clear_empties_storage():
    s = Storage()
    p = s.create_prompt(Prompt(title="X", content="Y"))
    s.create_collection(Collection(name="N"))
    s.clear()
    with pytest.raises(KeyError):
        s.get_prompt(p.id)
    assert s.get_collections() == []


def test_raise_on_missing_flag_behavior():
    s1 = Storage(raise_on_missing=True)
    with pytest.raises(KeyError):
        s1.get_prompt("NA")
    s2 = Storage(raise_on_missing=False)
    assert s2.get_prompt("NA") is None


def test_data_persistence_within_instance():
    s = Storage()
    p1 = s.create_prompt(Prompt(title="A", content="B"))
    assert s.get_prompt(p1.id) is not None
    s.create_prompt(Prompt(title="C", content="D"))
    assert len(s.get_prompts()) == 2