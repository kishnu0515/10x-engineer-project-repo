import pytest

# Robust import handling across different runners
try:
    from backend.app.models import Prompt
    from backend.app.storage import Storage
except ModuleNotFoundError:  # pragma: no cover
    import os
    import sys
    REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    BACKEND_PATH = os.path.join(REPO_ROOT, "backend")
    if BACKEND_PATH not in sys.path:
        sys.path.insert(0, BACKEND_PATH)
    try:
        from app.models import Prompt
        from app.storage import Storage
    except ModuleNotFoundError:
        if REPO_ROOT not in sys.path:
            sys.path.insert(0, REPO_ROOT)
        from backend.app.models import Prompt
        from backend.app.storage import Storage


def test_prompt_default_tags_empty():
    p = Prompt(title="T", content="C")
    assert hasattr(p, "tags")
    assert p.tags == []


def test_prompt_add_remove_has_list():
    p = Prompt(title="T", content="C")
    p.add_tag("Urgent")
    p.add_tag(" important ")
    # Normalized to lowercase and trimmed, deduped
    assert p.has_tag("urgent") is True
    assert p.has_tag("IMPORTANT") is True
    assert sorted(p.list_tags()) == ["important", "urgent"]

    # Removing tag that exists
    p.remove_tag("URGENT")
    assert p.has_tag("urgent") is False
    assert p.list_tags() == ["important"]


def test_prompt_add_tag_validation():
    p = Prompt(title="T", content="C")
    with pytest.raises(ValueError):
        p.add_tag("")
    with pytest.raises(ValueError):
        p.add_tag("   ")

    # Duplicate ignored (no error, but not added twice)
    p.add_tag("x")
    p.add_tag("X")
    assert p.list_tags() == ["x"]


def test_storage_filter_by_tag():
    s = Storage()
    p1 = Prompt(title="A", content="B")
    p1.add_tag("alpha")
    p2 = Prompt(title="C", content="D")
    p2.add_tag("beta")
    p3 = Prompt(title="E", content="F")
    p3.add_tag("Alpha")

    s.create_prompt(p1)
    s.create_prompt(p2)
    s.create_prompt(p3)

    # filter by tag (case-insensitive)
    results = s.get_prompts(tag="ALPHA")
    ids = [r.id for r in results]
    assert set(ids) == {p1.id, p3.id}

