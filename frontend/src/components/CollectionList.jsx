import React from "react";
import Button from "./Button.jsx";

export default function CollectionList({
  collections = [],
  selectedCollectionId = null,
  onSelectCollection,
  onCreateCollection,
  onDeleteCollection,
  isLoading = false,
  isSaving = false,
  error = null,
}) {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between gap-2">
        <div>
          <h2 className="text-sm font-semibold text-slate-900">Collections</h2>
          <p className="text-xs text-slate-500">Organize your prompts into groups.</p>
        </div>
        {onCreateCollection ? (
          <Button type="button" onClick={onCreateCollection} disabled={isSaving}>
            {isSaving ? "Creating..." : "New collection"}
          </Button>
        ) : null}
      </div>

      {isLoading ? (
        <div className="py-4 text-sm text-slate-500">Loading collections...</div>
      ) : error ? (
        <div className="rounded-md border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700">
          Failed to load collections.
        </div>
      ) : collections.length === 0 ? (
        <div className="rounded-md border border-dashed border-slate-200 bg-slate-50 px-3 py-4 text-sm text-slate-500">
          No collections yet. Create one to get started.
        </div>
      ) : (
        <ul className="divide-y divide-slate-200 rounded-md border border-slate-200 bg-white">
          {collections.map((c) => (
            <li key={c.id} className="flex items-center justify-between px-3 py-2 text-sm">
              <button
                type="button"
                onClick={() => onSelectCollection?.(c.id)}
                className={
                  "flex-1 truncate text-left " +
                  (selectedCollectionId === c.id
                    ? "font-semibold text-slate-900"
                    : "text-slate-800 hover:text-slate-900")
                }
              >
                {c.name}
              </button>
              {onDeleteCollection ? (
                <Button
                  type="button"
                  variant="ghost"
                  className="ml-2 px-2 py-1 text-[11px] text-rose-700 hover:bg-rose-50"
                  onClick={() => onDeleteCollection(c)}
                  disabled={isSaving}
                >
                  Delete
                </Button>
              ) : null}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
