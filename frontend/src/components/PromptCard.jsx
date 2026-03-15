import React from "react";

export default function PromptCard({ prompt, onClick, onEdit, onDelete }) {
  if (!prompt) return null;

  const { title, description, content, tags = [], updated_at: updatedAt } = prompt;

  const handleCardClick = () => {
    if (onClick) onClick(prompt);
  };

  return (
    <article
      className="flex cursor-pointer flex-col rounded-lg border border-slate-200 bg-white p-4 shadow-sm transition hover:-translate-y-0.5 hover:border-slate-300 hover:shadow"
      onClick={handleCardClick}
    >
      <header className="mb-2 flex items-start justify-between gap-2">
        <h3 className="line-clamp-1 text-sm font-semibold text-slate-900">{title}</h3>
        <div className="flex gap-1 text-xs text-slate-400">
          {updatedAt ? <span>Updated {new Date(updatedAt).toLocaleDateString()}</span> : null}
        </div>
      </header>

      {description ? (
        <p className="mb-2 line-clamp-2 text-xs text-slate-600">{description}</p>
      ) : null}

      <p className="mb-3 line-clamp-3 whitespace-pre-wrap text-xs text-slate-700">
        {content}
      </p>

      <footer className="mt-auto flex items-center justify-between gap-2">
        <div className="flex flex-wrap gap-1">
          {Array.isArray(tags) && tags.length > 0
            ? tags.slice(0, 3).map((tag) => (
                <span
                  key={tag}
                  className="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-slate-500"
                >
                  {tag}
                </span>
              ))
            : null}
          {Array.isArray(tags) && tags.length > 3 ? (
            <span className="text-[10px] text-slate-400">+{tags.length - 3} more</span>
          ) : null}
        </div>

        <div className="flex shrink-0 gap-1 text-xs">
          {onEdit ? (
            <button
              type="button"
              className="rounded border border-slate-200 bg-white px-2 py-1 text-xs text-slate-700 hover:bg-slate-50"
              onClick={(e) => {
                e.stopPropagation();
                onEdit(prompt);
              }}
            >
              Edit
            </button>
          ) : null}
          {onDelete ? (
            <button
              type="button"
              className="rounded border border-rose-200 bg-rose-50 px-2 py-1 text-xs text-rose-700 hover:bg-rose-100"
              onClick={(e) => {
                e.stopPropagation();
                onDelete(prompt);
              }}
            >
              Delete
            </button>
          ) : null}
        </div>
      </footer>
    </article>
  );
}
