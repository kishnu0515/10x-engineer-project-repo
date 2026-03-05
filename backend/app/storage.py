class Storage:
    """
    An in-memory storage class for managing prompts and collections.

    Attributes:
        _prompts (Dict[str, Prompt]): A dictionary to store prompts by their ID.
        _collections (Dict[str, Collection]): A dictionary to store collections by their ID.
    """

    def __init__(self):
        """
        Initializes the Storage class with empty dictionaries for prompts and collections.
        """
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """
        Adds a new prompt to the storage.

        Args:
            prompt (Prompt): The prompt to be added.

        Returns:
            Prompt: The prompt that was added.
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """
        Retrieves a prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The prompt with the specified ID, or None if not found.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """
        Retrieves all prompts.

        Returns:
            List[Prompt]: A list of all stored prompts.
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """
        Updates an existing prompt.

        Args:
            prompt_id (str): The ID of the prompt to update.
            prompt (Prompt): The new prompt data.

        Returns:
            Optional[Prompt]: The updated prompt, or None if the prompt ID does not exist.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """
        Deletes a prompt from the storage.

        Args:
            prompt_id (str): The ID of the prompt to delete.

        Returns:
            bool: True if the prompt was successfully deleted, False otherwise.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    def create_collection(self, collection: Collection) -> Collection:
        """
        Adds a new collection to the storage.

        Args:
            collection (Collection): The collection to be added.

        Returns:
            Collection: The collection that was added.
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """
        Retrieves a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to retrieve.

        Returns:
            Optional[Collection]: The collection with the specified ID, or None if not found.
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """
        Retrieves all collections.

        Returns:
            List[Collection]: A list of all stored collections.
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """
        Deletes a collection from the storage.

        Args:
            collection_id (str): The ID of the collection to delete.

        Returns:
            bool: True if the collection was successfully deleted, False otherwise.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """
        Retrieves prompts that belong to a specific collection.

        Args:
            collection_id (str): The ID of the collection.

        Returns:
            List[Prompt]: A list of prompts that are part of the collection.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    def clear(self):
        """
        Clears all prompts and collections from storage.
        """
        self._prompts.clear()
        self._collections.clear()
