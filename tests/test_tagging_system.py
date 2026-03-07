import pytest
from pydantic import ValidationError
from backend.app.models import Project  # Assuming Project is the model for tagging


def test_add_tag_to_project():
    project = Project(name="Project 1")
    project.add_tag("urgent")
    assert "urgent" in project.tags


def test_remove_tag_from_project():
    project = Project(name="Project 1", tags=["urgent"])
    project.remove_tag("urgent")
    assert "urgent" not in project.tags


def test_check_tag_exists_on_project():
    project = Project(name="Project 1", tags=["urgent", "important"])
    assert project.has_tag("urgent") is True
    assert project.has_tag("nonexistent") is False


def test_list_all_tags_on_project():
    project = Project(name="Project 1", tags=["urgent", "important", "review"])
    tags = project.list_tags()
    assert "urgent" in tags
    assert len(tags) == 3
