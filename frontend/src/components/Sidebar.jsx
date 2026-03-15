import React from "react";

function SidebarItem({ active, label, onClick, count }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={[
        "flex w-full items-center justify-between rounded-md px-3 py-2 text-left text-sm",
        active
          ? "bg-slate-900 text-white"
          : "text-slate-700 hover:bg-slate-100",
      ].join(" ")}
    >
      <span className="truncate">{label}</span>
      {typeof count === "number" ? (
        <span className={active ? "text-white/80" : "text-slate-400"}>{count}</span>
      ) : null}
    </button>
  );
}

export default function Sidebar({
  collections = [],
  selectedCollectionId = null,
  onSelectCollection,
  onClose,
}) {
  return (
    <aside className="flex h-full w-72 flex-col border-r border-slate-200 bg-white">
      <div className="flex items-center justify-between gap-2 border-b border-slate-200 px-4 py-3">
        <div>
          <div className="text-sm font-semibold text-slate-900">Collections</div>
          <div className="text-xs text-slate-500">Browse by group</div>
        </div>
        <button
          type="button"
          className="rounded-md border border-slate-200 bg-white px-2 py-1 text-xs text-slate-700 hover:bg-slate-50 md:hidden"
          onClick={onClose}
        >
          Close
        </button>
      </div>

      <div className="flex-1 overflow-auto p-3">
        <div className="space-y-1">
          <SidebarItem
            label="All prompts"
            active={selectedCollectionId === null}
            onClick={() => onSelectCollection?.(null)}
          />

          <div className="mt-3 px-1 text-xs font-semibold uppercase tracking-wide text-slate-400">
            Your collections
          </div>

          {collections.length === 0 ? (
            <div className="px-1 py-2 text-sm text-slate-500">No collections yet.</div>
          ) : (
            collections.map((c) => (
              <SidebarItem
                key={c.id}
                label={c.name}
                active={selectedCollectionId === c.id}
                onClick={() => onSelectCollection?.(c.id)}
              />
            ))
          )}
        </div>
      </div>

      <div className="border-t border-slate-200 p-3">
        <div className="rounded-md bg-slate-50 p-3 text-xs text-slate-600">
          Tip: use tags to filter prompts.
        </div>
      </div>
    </aside>
  );
}
