import React, { useEffect, useState } from "react";
import Button from "./Button.jsx";

export default function CollectionForm({
  initialCollection = null,
  onSubmit,
  onCancel,
  isSubmitting = false,
}) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [errors, setErrors] = useState({});

  const isEdit = Boolean(initialCollection && initialCollection.id);

  useEffect(() => {
    if (initialCollection) {
      setName(initialCollection.name ?? "");
      setDescription(initialCollection.description ?? "");
    }
  }, [initialCollection]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!onSubmit) return;

    const nextErrors = {};
    if (!name.trim()) {
      nextErrors.name = "Name is required.";
    }
    if (Object.keys(nextErrors).length > 0) {
      setErrors(nextErrors);
      return;
    }

    const payload = {
      name: name.trim(),
      description: description.trim() || null,
    };

    onSubmit(payload);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-1">
        <label className="block text-xs font-medium text-slate-700" htmlFor="collection-name">
          Name
        </label>
        <input
          id="collection-name"
          type="text"
          className="block w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm outline-none ring-0 placeholder:text-slate-400 focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
          value={name}
          onChange={(e) => {
            setName(e.target.value);
            if (errors.name) {
              setErrors((prev) => ({ ...prev, name: undefined }));
            }
          }}
          required
          minLength={1}
          aria-invalid={Boolean(errors.name)}
          aria-describedby={errors.name ? "collection-name-error" : undefined}
        />
        {errors.name ? (
          <p id="collection-name-error" className="text-xs text-rose-600">
            {errors.name}
          </p>
        ) : null}
      </div>

      <div className="space-y-1">
        <label className="block text-xs font-medium text-slate-700" htmlFor="collection-description">
          Description
        </label>
        <textarea
          id="collection-description"
          className="block w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm outline-none ring-0 placeholder:text-slate-400 focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
          rows={3}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Optional"
        />
      </div>

      <div className="flex justify-end gap-2 pt-2">
        {onCancel ? (
          <Button variant="secondary" type="button" onClick={onCancel}>
            Cancel
          </Button>
        ) : null}
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Saving..." : isEdit ? "Save changes" : "Create collection"}
        </Button>
      </div>
    </form>
  );
}
