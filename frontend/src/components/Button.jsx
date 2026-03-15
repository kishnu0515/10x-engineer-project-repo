import React from "react";

const baseClasses =
  "inline-flex items-center justify-center rounded-md px-3 py-1.5 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-slate-500 disabled:cursor-not-allowed disabled:opacity-60";

const variants = {
  primary:
    "bg-slate-900 text-white hover:bg-slate-800 border border-slate-900 focus:ring-offset-slate-900",
  secondary:
    "bg-white text-slate-800 border border-slate-200 hover:bg-slate-50",
  danger:
    "bg-rose-600 text-white border border-rose-600 hover:bg-rose-700 focus:ring-offset-rose-600",
  ghost:
    "bg-transparent text-slate-700 border border-transparent hover:bg-slate-100",
};

export default function Button({
  children,
  variant = "primary",
  className = "",
  as = "button",
  ...props
}) {
  const Component = as;
  const variantClasses = variants[variant] ?? variants.primary;

  return (
    <Component className={`${baseClasses} ${variantClasses} ${className}`} {...props}>
      {children}
    </Component>
  );
}
