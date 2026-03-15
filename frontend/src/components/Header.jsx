import React from "react";

export default function Header({ onToggleSidebar }) {
  return (
    <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/80 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-6xl items-center gap-3 px-4">
        <button
          type="button"
          className="inline-flex items-center justify-center rounded-md border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 md:hidden"
          onClick={onToggleSidebar}
          aria-label="Toggle sidebar"
        >
          Menu
        </button>

        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-slate-900 text-sm font-bold text-white">
            PL
          </div>
          <div className="leading-tight">
            <div className="text-sm font-semibold text-slate-900">PromptLab</div>
            <div className="text-xs text-slate-500">Prompts & collections</div>
          </div>
        </div>

        <div className="flex-1" />

        <nav className="hidden items-center gap-4 text-sm text-slate-600 md:flex">
          <a className="hover:text-slate-900" href="#/prompts">Prompts</a>
          <a className="hover:text-slate-900" href="#/collections">Collections</a>
          <a className="hover:text-slate-900" href="#/about">About</a>
        </nav>
      </div>
    </header>
  );
}
