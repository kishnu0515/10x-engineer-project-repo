"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique identifier using UUID4.

    Returns:
        A string representation of a UUID4.

    Example:
        >>> id = generate_id()
        >>> len(id)
        36
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Get the current UTC datetime.

    Returns:
        The current datetime in UTC.

    Example:
        >>> now = get_current_time()
        >>> isinstance(now, datetime)
        True
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for a prompt.

    Contains the common attributes shared between prompt creation and storage.

    Attributes:
        title: The title of the prompt (1-200 characters).
        content: The content of the prompt (must not be empty).
        description: Optional description of the prompt (max 500 characters).
        collection_id: Optional ID of the collection the prompt belongs to.
    """
    title: str = Field(..., min_length=1, max_length=200, description="The title of the prompt")
    content: str = Field(..., min_length=1, description="The content of the prompt")
    description: Optional[str] = Field(None, max_length=500, description="Optional description of the prompt")
    collection_id: Optional[str] = Field(None, description="Optional ID of the collection the prompt belongs to")


class PromptCreate(PromptBase):
    """Model for creating a new prompt.

    Inherits all fields from PromptBase.
    """
    pass


class PromptUpdate(PromptBase):
    """Model for updating an entire prompt.

    Requires all fields from PromptBase to replace the existing prompt.
    """
    pass


class PromptPartialUpdate(BaseModel):
    """Model for partially updating the fields of a prompt.

    Only provided fields will be updated; all fields are optional.

    Attributes:
        title: Optional new title of the prompt (1-200 characters).
        content: Optional new content of the prompt (must not be empty if provided).
        description: Optional new description of the prompt (max 500 characters).
        collection_id: Optional new ID of the collection the prompt belongs to.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Optional new title of the prompt")
    content: Optional[str] = Field(None, min_length=1, description="Optional new content of the prompt")
    description: Optional[str] = Field(None, max_length=500, description="Optional new description of the prompt")
    collection_id: Optional[str] = Field(None, description="Optional new ID of the collection the prompt belongs to")


class Prompt(PromptBase):
    """Database representation of a prompt.

    Complete prompt model with auto-generated ID and timestamps.

    Attributes:
        id: Unique identifier for the prompt (auto-generated UUID).
        created_at: Timestamp when the prompt was created (auto-generated).
        updated_at: Timestamp when the prompt was last updated (auto-generated).
    """
    id: str = Field(default_factory=generate_id, description="Unique identifier for the prompt")
    created_at: datetime = Field(default_factory=get_current_time, description="Timestamp when the prompt was created")
    updated_at: datetime = Field(default_factory=get_current_time, description="Timestamp when the prompt was last updated")

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base model for a collection.

    Contains the common attributes shared between collection creation and storage.

    Attributes:
        name: The name of the collection (1-100 characters).
        description: Optional description of the collection (max 500 characters).
    """
    name: str = Field(..., min_length=1, max_length=100, description="The name of the collection")
    description: Optional[str] = Field(None, max_length=500, description="Optional description of the collection")


class CollectionCreate(CollectionBase):
    """Model for creating a new collection.

    Inherits all fields from CollectionBase.
    """
    pass


class Collection(CollectionBase):
    """Database representation of a collection.

    Complete collection model with auto-generated ID and timestamp.

    Attributes:
        id: Unique identifier for the collection (auto-generated UUID).
        created_at: Timestamp when the collection was created (auto-generated).
    """
    id: str = Field(default_factory=generate_id, description="Unique identifier for the collection")
    created_at: datetime = Field(default_factory=get_current_time, description="Timestamp when the collection was created")

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Response model for a list of prompts.

    Used in API responses when returning multiple prompts.

    Attributes:
        prompts: List of Prompt objects.
        total: Total number of prompts in the list.
    """
    prompts: List[Prompt] = Field(..., description="List of Prompt objects")
    total: int = Field(..., description="Total number of prompts in the list")


class CollectionList(BaseModel):
    """Response model for a list of collections.

    Used in API responses when returning multiple collections.

    Attributes:
        collections: List of Collection objects.
        total: Total number of collections in the list.
    """
    collections: List[Collection] = Field(..., description="List of Collection objects")
    total: int = Field(..., description="Total number of collections in the list")


class HealthResponse(BaseModel):
    """Response model for the health status of the system.

    Used in health check endpoints to confirm the API is running.

    Attributes:
        status: Status of the system (e.g., "healthy").
        version: Version of the system.
    """
    status: str = Field(..., description="Status of the system")
    version: str = Field(..., description="Version of the system")

