import { request } from "./client.js";

/**
 * List prompts.
 * Supports optional filters: search, collection_id, tag, sort_by, sort_order.
 */
export async function getPrompts(params = {}) {
  // Backend returns: { prompts: Prompt[], total: number }
  return request("/prompts", { query: params });
}

export async function getPrompt(id) {
  if (!id) throw new Error("Prompt id is required");
  return request(`/prompts/${encodeURIComponent(id)}`);
}

export async function createPrompt(data) {
  if (!data) throw new Error("Prompt data is required");
  return request("/prompts", {
    method: "POST",
    body: data,
  });
}

export async function updatePrompt(id, data) {
  if (!id) throw new Error("Prompt id is required");
  if (!data) throw new Error("Prompt data is required");
  return request(`/prompts/${encodeURIComponent(id)}`, {
    method: "PUT",
    body: data,
  });
}

export async function deletePrompt(id) {
  if (!id) throw new Error("Prompt id is required");
  // Backend returns 204 No Content on success
  await request(`/prompts/${encodeURIComponent(id)}`, {
    method: "DELETE",
  });
  return true;
}
