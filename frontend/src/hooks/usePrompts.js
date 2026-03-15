import { useCallback, useEffect, useState } from "react";
import {
  getPrompts,
  getPrompt,
  createPrompt,
  updatePrompt,
  deletePrompt,
} from "../api/prompts.js";

export function usePrompts({ collectionId = null } = {}) {
  const [prompts, setPrompts] = useState([]);
  const [total, setTotal] = useState(0);
  const [selectedPrompt, setSelectedPrompt] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");

  const loadPrompts = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const params = {};
      if (collectionId) params.collection_id = collectionId;
      if (search) params.search = search;
      const data = await getPrompts(params);
      setPrompts(data.prompts || []);
      setTotal(data.total ?? data.prompts?.length ?? 0);
    } catch (err) {
      setError(err);
    } finally {
      setIsLoading(false);
    }
  }, [collectionId, search]);

  useEffect(() => {
    loadPrompts();
  }, [loadPrompts]);

  const refreshSelected = useCallback(
    async (id) => {
      if (!id) return;
      try {
        const data = await getPrompt(id);
        setSelectedPrompt(data);
      } catch (err) {
        // If not found (e.g. after delete), clear selection
        if (err && err.status === 404) {
          setSelectedPrompt(null);
        }
      }
    },
    [],
  );

  const handleCreate = useCallback(
    async (payload) => {
      setIsSaving(true);
      setError(null);
      try {
        const created = await createPrompt(payload);
        // Reload list to respect backend sorting/filtering
        await loadPrompts();
        setSelectedPrompt(created);
        return created;
      } catch (err) {
        setError(err);
        throw err;
      } finally {
        setIsSaving(false);
      }
    },
    [loadPrompts],
  );

  const handleUpdate = useCallback(
    async (id, payload) => {
      setIsSaving(true);
      setError(null);
      try {
        const updated = await updatePrompt(id, payload);
        await loadPrompts();
        setSelectedPrompt(updated);
        return updated;
      } catch (err) {
        setError(err);
        throw err;
      } finally {
        setIsSaving(false);
      }
    },
    [loadPrompts],
  );

  const handleDelete = useCallback(
    async (id) => {
      setIsSaving(true);
      setError(null);
      try {
        await deletePrompt(id);
        await loadPrompts();
        setSelectedPrompt(null);
      } catch (err) {
        setError(err);
        throw err;
      } finally {
        setIsSaving(false);
      }
    },
    [loadPrompts],
  );

  return {
    prompts,
    total,
    selectedPrompt,
    setSelectedPrompt,
    isLoading,
    isSaving,
    error,
    search,
    setSearch,
    reload: loadPrompts,
    createPrompt: handleCreate,
    updatePrompt: handleUpdate,
    deletePrompt: handleDelete,
    refreshSelected,
  };
}
