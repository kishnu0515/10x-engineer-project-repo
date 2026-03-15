import { useCallback, useEffect, useState } from "react";
import { getCollections, createCollection, deleteCollection } from "../api/collections.js";

export function useCollections() {
  const [collections, setCollections] = useState([]);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);

  const loadCollections = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getCollections();
      setCollections(data.collections || []);
      setTotal(data.total ?? data.collections?.length ?? 0);
    } catch (err) {
      setError(err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadCollections();
  }, [loadCollections]);

  const handleCreate = useCallback(
    async (payload) => {
      setIsSaving(true);
      setError(null);
      try {
        const created = await createCollection(payload);
        await loadCollections();
        return created;
      } catch (err) {
        setError(err);
        throw err;
      } finally {
        setIsSaving(false);
      }
    },
    [loadCollections],
  );

  const handleDelete = useCallback(
    async (id) => {
      setIsSaving(true);
      setError(null);
      try {
        await deleteCollection(id);
        await loadCollections();
      } catch (err) {
        setError(err);
        throw err;
      } finally {
        setIsSaving(false);
      }
    },
    [loadCollections],
  );

  return {
    collections,
    total,
    isLoading,
    isSaving,
    error,
    reload: loadCollections,
    createCollection: handleCreate,
    deleteCollection: handleDelete,
  };
}
