import React, { useMemo, useState } from "react";
import Header from "./Header.jsx";
import Sidebar from "./Sidebar.jsx";

export default function Layout({
  collections = [],
  selectedCollectionId = null,
  onSelectCollection,
  children,
}) {
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  const selectedCollection = useMemo(() => {
    if (!selectedCollectionId) return null;
    return collections.find((c) => c.id === selectedCollectionId) ?? null;
  }, [collections, selectedCollectionId]);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Header onToggleSidebar={() => setMobileSidebarOpen((v) => !v)} />

      <div className="mx-auto flex max-w-6xl">
        {/* Desktop sidebar */}
        <div className="hidden h-[calc(100vh-3.5rem)] md:block">
          <Sidebar
            collections={collections}
            selectedCollectionId={selectedCollectionId}
            onSelectCollection={onSelectCollection}
          />
        </div>

        {/* Mobile sidebar overlay */}
        {mobileSidebarOpen ? (
          <div className="fixed inset-0 z-20 md:hidden">
            <div
              className="absolute inset-0 bg-black/40"
              onClick={() => setMobileSidebarOpen(false)}
              aria-hidden="true"
            />
            <div className="absolute left-0 top-0 h-full">
              <Sidebar
                collections={collections}
                selectedCollectionId={selectedCollectionId}
                onSelectCollection={(id) => {
                  onSelectCollection?.(id);
                  setMobileSidebarOpen(false);
                }}
                onClose={() => setMobileSidebarOpen(false)}
              />
            </div>
          </div>
        ) : null}

        <main className="flex-1 p-4">
          <div className="mb-4">
            <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">
              {selectedCollection ? "Collection" : "Workspace"}
            </div>
            <div className="text-xl font-semibold text-slate-900">
              {selectedCollection ? selectedCollection.name : "All prompts"}
            </div>
          </div>

          {children}
        </main>
      </div>
    </div>
  );
}
