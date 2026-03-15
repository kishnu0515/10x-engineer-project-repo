import { request } from "./client.js";

export async function getCollections() {
  // Backend returns: { collections: Collection[], total: number }
  return request("/collections");
}

export async function createCollection(data) {
  if (!data) throw new Error("Collection data is required");
  return request("/collections", {
    method: "POST",
    body: data,
  });
}

export async function deleteCollection(id) {
  if (!id) throw new Error("Collection id is required");
  await request(`/collections/${encodeURIComponent(id)}`, {
    method: "DELETE",
  });
  return true;
}
