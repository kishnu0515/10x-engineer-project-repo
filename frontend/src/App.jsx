import React, { useMemo, useState } from "react";
import Layout from "./components/Layout.jsx";
import PromptList from "./components/PromptList.jsx";
import PromptDetail from "./components/PromptDetail.jsx";
import PromptForm from "./components/PromptForm.jsx";
import CollectionList from "./components/CollectionList.jsx";
import Modal from "./components/Modal.jsx";
import Button from "./components/Button.jsx";
import SearchBar from "./components/SearchBar.jsx";
import LoadingSpinner from "./components/LoadingSpinner.jsx";
import ErrorMessage from "./components/ErrorMessage.jsx";
import { usePrompts } from "./hooks/usePrompts.js";
import { useCollections } from "./hooks/useCollections.js";

export default function App() {
  const [selectedCollectionId, setSelectedCollectionId] = useState(null);
  const [isPromptModalOpen, setIsPromptModalOpen] = useState(false);
  const [editingPrompt, setEditingPrompt] = useState(null);
  const [confirmDeletePrompt, setConfirmDeletePrompt] = useState(null);
  const [confirmDeleteCollection, setConfirmDeleteCollection] = useState(null);

  const {
    collections,
    isLoading: collectionsLoading,
    isSaving: collectionsSaving,
    error: collectionsError,
    createCollection,
    deleteCollection,
  } = useCollections();

  const {
    prompts,
    selectedPrompt,
    setSelectedPrompt,
    isLoading: promptsLoading,
    isSaving: promptsSaving,
    error: promptsError,
    search,
    setSearch,
    createPrompt,
    updatePrompt,
    deletePrompt,
  } = usePrompts({ collectionId: selectedCollectionId });

  const hasError = promptsError || collectionsError;

  const handleOpenCreatePrompt = () => {
    setEditingPrompt(null);
    setIsPromptModalOpen(true);
  };

  const handleEditPrompt = (prompt) => {
    setEditingPrompt(prompt);
    setIsPromptModalOpen(true);
  };

  const handleSubmitPrompt = async (payload) => {
    if (editingPrompt) {
      await updatePrompt(editingPrompt.id, payload);
    } else {
      await createPrompt(payload);
    }
    setIsPromptModalOpen(false);
    setEditingPrompt(null);
  };

  const handleConfirmDeletePrompt = (prompt) => {
    setConfirmDeletePrompt(prompt);
  };

  const handleDeletePrompt = async () => {
    if (!confirmDeletePrompt) return;
    await deletePrompt(confirmDeletePrompt.id);
    setConfirmDeletePrompt(null);
  };

  const handleCreateCollection = async (payload) => {
    await createCollection(payload);
  };

  const handleConfirmDeleteCollection = (collection) => {
    setConfirmDeleteCollection(collection);
  };

  const handleDeleteCollection = async () => {
    if (!confirmDeleteCollection) return;
    await deleteCollection(confirmDeleteCollection.id);
    if (selectedCollectionId === confirmDeleteCollection.id) {
      setSelectedCollectionId(null);
    }
    setConfirmDeleteCollection(null);
  };

  const layoutCollections = useMemo(() => collections || [], [collections]);

  return (
    <Layout
      collections={layoutCollections}
      selectedCollectionId={selectedCollectionId}
      onSelectCollection={(id) => {
        setSelectedCollectionId(id);
        setSelectedPrompt(null);
      }}
    >
      <div className="flex flex-col gap-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <SearchBar value={search} onChange={setSearch} />

          <div className="flex flex-wrap items-center gap-2">
            <Button
              type="button"
              variant="secondary"
              onClick={handleOpenCreatePrompt}
              disabled={promptsSaving}
            >
              New prompt
            </Button>
          </div>
        </div>

        {hasError ? (
          <ErrorMessage
            title="Failed to load data"
            message={hasError.message || "Please try again."}
          />
        ) : null}

        {promptsLoading ? (
          <LoadingSpinner label="Loading prompts..." />
        ) : (
          <PromptList
            prompts={prompts}
            isLoading={promptsLoading}
            error={promptsError}
            onSelectPrompt={setSelectedPrompt}
            onEditPrompt={handleEditPrompt}
            onDeletePrompt={handleConfirmDeletePrompt}
          />
        )}

        <div className="grid gap-4 md:grid-cols-[2fr,1fr]">
          <div>
            <PromptDetail
              prompt={selectedPrompt}
              onBack={() => setSelectedPrompt(null)}
              onEdit={handleEditPrompt}
              onDelete={handleConfirmDeletePrompt}
            />
          </div>

          <div>
            <CollectionList
              collections={layoutCollections}
              selectedCollectionId={selectedCollectionId}
              onSelectCollection={setSelectedCollectionId}
              onDeleteCollection={handleConfirmDeleteCollection}
              onCreateCollection={() => {
                // For now, just create a simple collection from a prompt.
                const name = window.prompt("Collection name");
                if (name) handleCreateCollection({ name });
              }}
              isLoading={collectionsLoading}
              isSaving={collectionsSaving}
              error={collectionsError}
            />
          </div>
        </div>
      </div>

      {/* Prompt create/edit modal */}
      <Modal
        open={isPromptModalOpen}
        title={editingPrompt ? "Edit prompt" : "New prompt"}
        onClose={() => {
          setIsPromptModalOpen(false);
          setEditingPrompt(null);
        }}
        size="lg"
      >
        <PromptForm
          initialPrompt={editingPrompt}
          onSubmit={handleSubmitPrompt}
          onCancel={() => {
            setIsPromptModalOpen(false);
            setEditingPrompt(null);
          }}
          isSubmitting={promptsSaving}
        />
      </Modal>

      {/* Prompt delete confirmation modal */}
      <Modal
        open={Boolean(confirmDeletePrompt)}
        title="Delete prompt"
        description="This action cannot be undone."
        onClose={() => setConfirmDeletePrompt(null)}
      >
        <p className="text-sm text-slate-700">
          Are you sure you want to delete
          {" "}
          <span className="font-semibold">{confirmDeletePrompt?.title}</span>?
        </p>
        <div className="mt-4 flex justify-end gap-2">
          <Button
            type="button"
            variant="secondary"
            onClick={() => setConfirmDeletePrompt(null)}
          >
            Cancel
          </Button>
          <Button
            type="button"
            variant="danger"
            onClick={handleDeletePrompt}
            disabled={promptsSaving}
          >
            {promptsSaving ? "Deleting..." : "Delete"}
          </Button>
        </div>
      </Modal>

      {/* Collection delete confirmation modal */}
      <Modal
        open={Boolean(confirmDeleteCollection)}
        title="Delete collection"
        description="This will not delete prompts, but they will no longer belong to this collection."
        onClose={() => setConfirmDeleteCollection(null)}
      >
        <p className="text-sm text-slate-700">
          Are you sure you want to delete
          {" "}
          <span className="font-semibold">{confirmDeleteCollection?.name}</span>?
        </p>
        <div className="mt-4 flex justify-end gap-2">
          <Button
            type="button"
            variant="secondary"
            onClick={() => setConfirmDeleteCollection(null)}
          >
            Cancel
          </Button>
          <Button
            type="button"
            variant="danger"
            onClick={handleDeleteCollection}
            disabled={collectionsSaving}
          >
            {collectionsSaving ? "Deleting..." : "Delete"}
          </Button>
        </div>
      </Modal>
    </Layout>
  );
}
