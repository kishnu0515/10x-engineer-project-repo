import React, { useEffect, useId } from "react";
import Button from "./Button.jsx";

export default function Modal({
  open,
  title,
  description,
  children,
  onClose,
  size = "md", // md | lg
}) {
  const titleId = useId();

  useEffect(() => {
    if (!open || !onClose) return;

    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        event.stopPropagation();
        onClose();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [open, onClose]);

  if (!open) return null;

  const widthClass = size === "lg" ? "max-w-2xl" : "max-w-md";

  return (
    <div
      className="fixed inset-0 z-40 flex items-center justify-center bg-black/40 p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby={titleId}
    >
      <div className={`w-full ${widthClass} rounded-lg border border-slate-200 bg-white shadow-xl`}>
        <header className="border-b border-slate-200 px-4 py-3">
          <div className="flex items-center justify-between gap-2">
            <div>
              <h2 id={titleId} className="text-sm font-semibold text-slate-900">
                {title}
              </h2>
              {description ? (
                <p className="mt-1 text-xs text-slate-500">{description}</p>
              ) : null}
            </div>
            {onClose ? (
              <Button
                variant="ghost"
                type="button"
                className="px-2 py-1 text-[11px]"
                onClick={onClose}
              >
                Close
              </Button>
            ) : null}
          </div>
        </header>
        <div className="px-4 py-3">{children}</div>
      </div>
    </div>
  );
}
