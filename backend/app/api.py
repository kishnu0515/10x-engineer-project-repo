

# ============== Health Check ==============

@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    """Check the health status of the API.
    
    Returns:
        HealthResponse: A health status object containing status and version.
        
    Raises:
        HTTPException: If internal error occurs (500).
    """
    try:
        return HealthResponse(status="healthy", version="1.0.0")
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")


# ============== Prompt Endpoints ==============

@router.get("/prompts", response_model=PromptList)
def list_prompts(
    search: Optional[str] = Query(None, description="Search term to filter prompts by title"),
    collection_id: Optional[str] = Query(None, description="Collection ID to filter prompts"),
    skip: int = Query(0, ge=0, description="Number of prompts to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of prompts to return")
) -> PromptList:
    """Retrieve a paginated list of prompts with optional filtering.
    
    Args:
        search (str): Optional search string to filter prompts by title.
        collection_id (str): Optional collection ID to filter prompts by collection.
        skip (int): Number of prompts to skip (pagination offset).
        limit (int): Maximum number of prompts to return (pagination limit).
        
    Returns:
        PromptList: A list of prompts and total count.
        
    Raises:
        HTTPException: If internal error occurs (500).
    """
    try:
        prompts = storage.get_prompts(search=search, collection_id=collection_id)
        paginated = prompts[skip : skip + limit]
        return PromptList(prompts=paginated, total=len(prompts))
    except Exception as e:
        logger.error(f"Failed to list prompts: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str) -> Prompt:
    """Retrieve a specific prompt by its unique identifier.
    
    Args:
        prompt_id (str): The unique identifier of the prompt to retrieve.
        
    Returns:
        Prompt: The requested Prompt object.
        
    Raises:
        HTTPException: If the prompt is not found (404) or internal error (500).
    """
    try:
        prompt = storage.get_prompt(prompt_id)
        if not prompt:
            raise HTTPException(status_code=404, detail="Prompt not found")
        return prompt
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get prompt {prompt_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate) -> Prompt:
    """Create a new prompt.
    
    Args:
        prompt_data (PromptCreate): The PromptCreate object containing prompt details.
        
    Returns:
        Prompt: The created Prompt object with auto-generated ID and timestamps.
        
    Raises:
        HTTPException: If validation fails (400) or internal error (500).
    """
    try:
        prompt = Prompt(**prompt_data.model_dump())
        created = storage.create_prompt(prompt)
        logger.info(f"Created prompt {created.id}")
        return created
    except ValueError as e:
        logger.warning(f"Validation error creating prompt: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create prompt: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate) -> Prompt:
    """Completely replace an existing prompt (all fields required).
    
    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): The PromptUpdate object with complete replacement data.
        
    Returns:
        Prompt: The updated Prompt object with new timestamp.
        
    Raises:
        HTTPException: If prompt not found (404), validation fails (400), or internal error (500).
    """
    try:
        existing = storage.get_prompt(prompt_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Prompt not found")
        
        updated = storage.update_prompt(prompt_id, prompt_data)
        logger.info(f"Updated prompt {prompt_id}")
        return updated
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Validation error updating prompt {prompt_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to update prompt {prompt_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/prompts/{prompt_id}", response_model=Prompt)
def partial_update_prompt(prompt_id: str, prompt_data: PromptPartialUpdate) -> Prompt:
    """Partially update an existing prompt (only provided fields updated).
    
    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptPartialUpdate): The PromptPartialUpdate object with fields to update.
        
    Returns:
        Prompt: The updated Prompt object with new timestamp.
        
    Raises:
        HTTPException: If prompt not found (404), validation fails (400), or internal error (500).
    """
    try:
        existing = storage.get_prompt(prompt_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Prompt not found")
        
        updated = storage.partial_update_prompt(prompt_id, prompt_data)
        logger.info(f"Partially updated prompt {prompt_id}")
        return updated
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Validation error patching prompt {prompt_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to patch prompt {prompt_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str) -> None:
    """Delete a prompt by its unique identifier.
    
    Args:
        prompt_id (str): The unique identifier of the prompt to delete.
        
    Raises:
        HTTPException: If prompt not found (404) or internal error (500).
    """
    try:
        existing = storage.get_prompt(prompt_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Prompt not found")
        
        storage.delete_prompt(prompt_id)
        logger.info(f"Deleted prompt {prompt_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete prompt {prompt_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ============== Collection Endpoints ==============

@router.get("/collections", response_model=CollectionList)
def list_collections(
    skip: int = Query(0, ge=0, description="Number of collections to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of collections to return")
) -> CollectionList:
    """Retrieve a paginated list of all collections.
    
    Args:
        skip (int): Number of collections to skip (pagination offset).
        limit (int): Maximum number of collections to return (pagination limit).
        
    Returns:
        CollectionList: A list of collections and total count.
        
    Raises:
        HTTPException: If internal error occurs (500).
    """
    try:
        collections = storage.get_collections()
        paginated = collections[skip : skip + limit]
        return CollectionList(collections=paginated, total=len(collections))
    except Exception as e:
        logger.error(f"Failed to list collections: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str) -> Collection:
    """Retrieve a specific collection by its unique identifier.
    
    Args:
        collection_id (str): The unique identifier of the collection to retrieve.
        
    Returns:
        Collection: The requested Collection object.
        
    Raises:
        HTTPException: If collection not found (404) or internal error (500).
    """
    try:
        collection = storage.get_collection(collection_id)
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        return collection
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get collection {collection_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate) -> Collection:
    """Create a new collection.
    
    Args:
        collection_data (CollectionCreate): The CollectionCreate object containing collection details.
        
    Returns:
        Collection: The created Collection object with auto-generated ID and timestamp.
        
    Raises:
        HTTPException: If validation fails (400) or internal error (500).
    """
    try:
        collection = Collection(**collection_data.model_dump())
        created = storage.create_collection(collection)
        logger.info(f"Created collection {created.id}")
        return created
    except ValueError as e:
        logger.warning(f"Validation error creating collection: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create collection: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str) -> None:
    """Delete a collection by its unique identifier.
    
    Note:
        Deleting a collection will orphan prompts that belong to it.
        Consider implementing cascade delete or nullifying collection_id in prompts.
    
    Args:
        collection_id (str): The unique identifier of the collection to delete.
        
    Raises:
        HTTPException: If collection not found (404) or internal error (500).
    """
    try:
        existing = storage.get_collection(collection_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Collection not found")
        
        storage.delete_collection(collection_id)
        logger.info(f"Deleted collection {collection_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete collection {collection_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


app = FastAPI(title="PromptLab API", version="1.0.0")
app.include_router(router)
