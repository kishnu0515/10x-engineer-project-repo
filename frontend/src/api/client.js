const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function buildUrl(path, query) {
  const base = API_BASE_URL.replace(/\/$/, "");
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  const url = new URL(base + cleanPath);

  if (query && typeof query === "object") {
    Object.entries(query).forEach(([key, value]) => {
      if (value === undefined || value === null || value === "") return;
      url.searchParams.set(key, String(value));
    });
  }

  return url.toString();
}

async function request(path, { method = "GET", headers = {}, body, query } = {}) {
  const url = buildUrl(path, query);

  const finalHeaders = {
    Accept: "application/json",
    ...headers,
  };

  let finalBody = body;
  if (body && typeof body === "object" && !(body instanceof FormData)) {
    finalHeaders["Content-Type"] = finalHeaders["Content-Type"] || "application/json";
    finalBody = JSON.stringify(body);
  }

  let response;
  try {
    response = await fetch(url, {
      method,
      headers: finalHeaders,
      body: finalBody,
    });
  } catch (networkError) {
    const error = new Error("Network error. Please check your connection.");
    error.cause = networkError;
    error.isNetworkError = true;
    throw error;
  }

  const contentType = response.headers.get("Content-Type") || "";
  const isJson = contentType.includes("application/json");

  let data;
  if (isJson) {
    try {
      data = await response.json();
    } catch {
      data = null;
    }
  } else {
    data = await response.text().catch(() => null);
  }

  if (!response.ok) {
    const error = new Error(
      (data && (data.detail || data.error_message || data.message)) ||
        `Request failed with status ${response.status}`,
    );
    error.status = response.status;
    error.data = data;
    throw error;
  }

  return data;
}

export { API_BASE_URL, request };
