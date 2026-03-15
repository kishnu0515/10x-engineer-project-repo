import React from "react";

export default function ErrorMessage({
  title = "Something went wrong",
  message = "Please try again.",
  onRetry,
}) {
  return (
    <div className="rounded-md border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700">
      <div className="font-medium">{title}</div>
      {message ? <div className="mt-0.5 text-xs">{message}</div> : null}
      {onRetry ? (
        <button
          type="button"
          className="mt-2 text-xs font-medium text-rose-800 underline underline-offset-2 hover:text-rose-900"
          onClick={onRetry}
        >
          Try again
        </button>
      ) : null}
    </div>
  );
}
