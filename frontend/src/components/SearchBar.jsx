import React from "react";

export default function SearchBar({
  value,
  onChange,
  placeholder = "Search prompts...",
}) {
  return (
    <div className="relative w-full max-w-sm">
      <input
        type="search"
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
        placeholder={placeholder}
        aria-label={placeholder}
        className="block w-full rounded-md border border-slate-300 bg-white px-3 py-2 pl-8 text-sm text-slate-900 shadow-sm outline-none ring-0 placeholder:text-slate-400 focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
      />
      <span
        className="pointer-events-none absolute inset-y-0 left-2 flex items-center text-slate-400"
        aria-hidden="true"
      >
        🔍
      </span>
    </div>
  );
}
