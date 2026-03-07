
class Storage:
    """In-memory storage for prompts and collections.

    Methods:
        create_prompt(prompt): Stores a new prompt in storage.
        get_prompt(prompt_id): Retrieves a prompt by ID.
        get_prompts(search, collection_id): Retrieves prompts with optional filtering.
        update_prompt(prompt_id, prompt_data): Updates an existing prompt.
        partial_update_prompt(prompt_id, prompt_data): Partially updates a prompt.
        delete_prompt(prompt_id): Deletes a prompt by ID.
        create_collection(collection): Stores a new collection in storage.
        get_collection(collection_id): Retrieves a collection by ID.
        get_collections(): Retrieves all collections.
        delete_collection(collection_id): Deletes a collection by ID.
        clear(): Clears all prompts and collections from storage.
    """

    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}

    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Store a new prompt in storage.

        Args:
            prompt (Prompt): The prompt to store.

        Returns:
            Prompt: The stored prompt.
        """
        self._prompts[prompt.id] = prompt
        return prompt

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its unique identifier.

        Args:
            prompt_id (str): The unique identifier of the prompt.

        Returns:
            Optional[Prompt]: The requested prompt if found, None otherwise.
        """
        return self._prompts.get(prompt_id)

    def get_prompts(
        self,
        search: Optional[str] = None,
        collection_id: Optional[str] = None,
    ) -> List[Prompt]:
        """Retrieve prompts with optional filtering by search term or collection.

        Args:
            search (Optional[str]): Search string to filter prompts by title.
            collection_id (Optional[str]): ID of the collection to filter prompts.

        Returns:
            List[Prompt]: A list of prompts that match the filter criteria.
        """
        results = list(self._prompts.values())
        if search:
            normalized_search = search.strip().lower()
            results = [prompt for prompt in results if normalized_search in prompt.title.lower()]
        if collection_id:
            results = [prompt for prompt in results if prompt.collection_id == collection_id]
        return sorted(results, key=lambda prompt: prompt.updated_at, reverse=True)

    def update_prompt(self, prompt_id: str, prompt_data: PromptUpdate) -> Optional[Prompt]:
        """Update an existing prompt with new data.

        Args:
            prompt_id (str): The unique identifier of the prompt to update.
            prompt_data (PromptUpdate): The data to update the prompt with.

        Returns:
            Optional[Prompt]: The updated prompt if successful, None if not found.
        """
        existing = self._prompts.get(prompt_id)
        if not existing:
            return None
        updated_values = {**prompt_data.model_dump(), "updated_at": get_current_timestamp()}
        updated = existing.model_copy(update=updated_values)
        self._prompts[prompt_id] = updated
        return updated

    def partial_update_prompt(self, prompt_id: str, prompt_data: PromptPartialUpdate) -> Optional[Prompt]:
        """Partially update a prompt with provided fields.

        Args:
            prompt_id (str): The unique identifier of the prompt to update.
            prompt_data (PromptPartialUpdate): Partial data to update the prompt.

        Returns:
            Optional[Prompt]: The updated prompt if successful, None if not found.
        """
        existing = self._prompts.get(prompt_id)
        if not existing:
            return None
        updates = prompt_data.model_dump(exclude_unset=True)
        if not updates:
            return existing
        updates["updated_at"] = get_current_timestamp()
        updated = existing.model_copy(update=updates)
        self._prompts[prompt_id] = updated
        return updated

    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by its unique identifier.

        Args:
            prompt_id (str): The unique identifier of the prompt to delete.

        Returns:
            bool: True if the prompt was deleted, False if it was not found.
        """
        return self._prompts.pop(prompt_id, None) is not None

    def create_collection(self, collection: Collection) -> Collection:
        """Store a new collection in storage.

        Args:
            collection (Collection): The collection to store.

        Returns:
            Collection: The stored collection.
        """
        self._collections[collection.id] = collection
        return collection

    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its unique identifier.

        Args:
            collection_id (str): The unique identifier of the collection.

        Returns:
            Optional[Collection]: The requested collection if found, None otherwise.
        """
        return self._collections.get(collection_id)

    def get_collections(self) -> List[Collection]:
        """Retrieve all collections, sorted by creation date.

        Returns:
            List[Collection]: A list of all stored collections.
        """
        return sorted(
            self._collections.values(),
            key=lambda collection: collection.created_at,
            reverse=True,
        )

    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by its unique identifier.

        Args:
            collection_id (str): The unique identifier of the collection to delete.

        Returns:
            bool: True if the collection was deleted, False if it was not found.
        """
        return self._collections.pop(collection_id, None) is not None

    def clear(self) -> None:
        """Clear all stored prompts and collections.

        This method deletes all prompts and collections.
        """
        self._prompts.clear()
        self._collections.clear()
