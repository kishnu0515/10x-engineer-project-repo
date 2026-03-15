import React, { useEffect, useState } from "react";

export default function PromptForm({
  initialPrompt = null,
  onSubmit,
  onCancel,
  isSubmitting = false,
}) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [description, setDescription] = useState("");
  const [collectionId, setCollectionId] = useState("");
  const [tagsInput, setTagsInput] = useState("");
  const [errors, setErrors] = useState({});

  const isEdit = Boolean(initialPrompt && initialPrompt.id);

  useEffect(() => {
    if (initialPrompt) {
      setTitle(initialPrompt.title ?? "");
      setContent(initialPrompt.content ?? "");
      setDescription(initialPrompt.description ?? "");
      setCollectionId(initialPrompt.collection_id ?? "");
      if (Array.isArray(initialPrompt.tags)) {
        setTagsInput(initialPrompt.tags.join(", "));
      }
    }
  }, [initialPrompt]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!onSubmit) return;

    const nextErrors = {};
    if (!title.trim()) {
      nextErrors.title = "Title is required.";
    }
    if (!content.trim()) {
      nextErrors.content = "Content is required.";
    }

    if (Object.keys(nextErrors).length > 0) {
      setErrors(nextErrors);
      return;
    }

    const tags = tagsInput
      .split(",")
      .map((t) => t.trim())
      .filter(Boolean);

    const payload = {
      title: title.trim(),
      content: content.trim(),
      description: description.trim() || null,
      collection_id: collectionId.trim() || null,
      tags,
    };

    onSubmit(payload);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-1">
        <label className="block text-xs font-medium text-slate-700" htmlFor="title">
          Title
        </label>
        <input
          id="title"
          type="text"
          className="block w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm outline-none ring-0 placeholder:text-slate-400 focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            if (errors.title) {
              setErrors((prev) => ({ ...prev, title: undefined }));
            }
          }}
          required
          minLength={1}
          aria-invalid={Boolean(errors.title)}
          aria-describedby={errors.title ? "title-error" : undefined}
        />
        {errors.title ? (
          <p id="title-error" className="text-xs text-rose-600">
            {errors.title}
          </p>
        ) : null}
      </div>

      <div className="space-y-1">
        <label className="block text-xs font-medium text-slate-700" htmlFor="description">
          Description
        </label>
        <textarea
          id="description"
          className="block w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm outline-none ring-0 placeholder:text-slate-400 focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
          rows={2}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>

      <div className="space-y-1">
        <label className="block text-xs font-medium text-slate-700" htmlFor="content">
          Prompt content
        </label>
        <textarea
          id="content"
          className="block w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm outline-none ring-0 placeholder:text-slate-400 focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
          rows={6}
          value={content}
          onChange={(e) => {
            setContent(e.target.value);
            if (errors.content) {
              setErrors((prev) => ({ ...prev, content: undefined }));
            }
          }}
          required
          minLength={1}
          aria-invalid={Boolean(errors.content)}
          aria-describedby={errors.content ? "content-error" : undefined}
        />
        {errors.content ? (
          <p id="content-error" className="text-xs text-rose-600">
            {errors.content}
          </p>
        ) : null}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-1">
          <label className="block text-xs font-medium text-slate-700" htmlFor="collectionId">
            Collection ID
          </label>
          <input
            id="collectionId"
            type="text"
            className="block w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm outline-none ring-0 placeholder:text-slate-400 focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
            value={collectionId}
            onChange={(e) => setCollectionId(e.target.value)}
            placeholder="Optional"
          />
        </div>

        <div className="space-y-1">
          <label className="block text-xs font-medium text-slate-700" htmlFor="tags">
            Tags
          </label>
          <input
            id="tags"
            type="text"
            className="block w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm outline-none ring-0 placeholder:text-slate-400 focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
            value={tagsInput}
            onChange={(e) => setTagsInput(e.target.value)}
            placeholder="e.g. writing, brainstorming"
          />
          <p className="text-[11px] text-slate-500">Comma-separated; will be normalized on the backend.</p>
        </div>
      </div>

      <div className="flex justify-end gap-2 pt-2">
        {onCancel ? (
          <button
            type="button"
            className="rounded-md border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50"
            onClick={onCancel}
          >
            Cancel
          </button>
        ) : null}
        <button
          type="submit"
          className="inline-flex items-center justify-center rounded-md bg-slate-900 px-3 py-1.5 text-xs font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Saving..." : isEdit ? "Save changes" : "Create prompt"}
        </button>
      </div>
    </form>
  );
}
