import React from "react";
import PromptCard from "./PromptCard.jsx";

export default function PromptList({
  prompts = [],
  isLoading = false,
  error = null,
  onSelectPrompt,
  onEditPrompt,
  onDeletePrompt,
  emptyMessage = "No prompts yet. Create your first one!",
}) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12 text-sm text-slate-500">
        Loading prompts...
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">
        Failed to load prompts.
      </div>
    );
  }

  if (!prompts || prompts.length === 0) {
    return (
      <div className="flex items-center justify-center py-12 text-sm text-slate-500">
        {emptyMessage}
      </div>
    );
  }

  return (
    <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
      {prompts.map((prompt) => (
        <PromptCard
          key={prompt.id}
          prompt={prompt}
          onClick={onSelectPrompt}
          onEdit={onEditPrompt}
          onDelete={onDeletePrompt}
        />
      ))}
    </div>
  );
}
