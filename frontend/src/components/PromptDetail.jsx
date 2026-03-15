import React from "react";

export default function PromptDetail({ prompt, onBack, onEdit, onDelete }) {
  if (!prompt) {
    return (
      <div className="rounded-lg border border-slate-200 bg-white p-4 text-sm text-slate-500">
        Select a prompt to view details.
      </div>
    );
  }

  const {
    title,
    description,
    content,
    tags = [],
    created_at: createdAt,
    updated_at: updatedAt,
    collection_id: collectionId,
  } = prompt;

  return (
    <article className="space-y-4 rounded-lg border border-slate-200 bg-white p-4">
      <header className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
          {description ? (
            <p className="mt-1 text-sm text-slate-600">{description}</p>
          ) : null}

          <div className="mt-2 flex flex-wrap items-center gap-2 text-[11px] text-slate-500">
            {collectionId ? <span>Collection: {collectionId}</span> : null}
            {createdAt ? <span>Created: {new Date(createdAt).toLocaleString()}</span> : null}
            {updatedAt ? <span>Updated: {new Date(updatedAt).toLocaleString()}</span> : null}
          </div>
        </div>

        <div className="flex flex-wrap items-center justify-end gap-2">
          {onBack ? (
            <button
              type="button"
              className="rounded-md border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50"
              onClick={onBack}
            >
              Back
            </button>
          ) : null}
          {onEdit ? (
            <button
              type="button"
              className="rounded-md border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50"
              onClick={() => onEdit(prompt)}
            >
              Edit
            </button>
          ) : null}
          {onDelete ? (
            <button
              type="button"
              className="rounded-md border border-rose-200 bg-rose-50 px-3 py-1.5 text-xs font-medium text-rose-700 hover:bg-rose-100"
              onClick={() => onDelete(prompt)}
            >
              Delete
            </button>
          ) : null}
        </div>
      </header>

      <section>
        <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
          Prompt
        </h3>
        <pre className="whitespace-pre-wrap rounded-md bg-slate-50 p-3 text-sm text-slate-800">
          {content}
        </pre>
      </section>

      <section>
        <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
          Tags
        </h3>
        {Array.isArray(tags) && tags.length > 0 ? (
          <div className="flex flex-wrap gap-1">
            {tags.map((tag) => (
              <span
                key={tag}
                className="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-slate-500"
              >
                {tag}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500">No tags.</p>
        )}
      </section>
    </article>
  );
}
