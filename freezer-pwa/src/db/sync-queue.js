import { db } from "./schema.js";
import { syncOffline } from "../api/items.js";

export async function enqueue(entity, type, data) {
  await db.sync_queue.add({
    entity,
    type,
    data,
    client_updated_at: new Date().toISOString(),
  });
}

export async function flushQueue() {
  const pending = await db.sync_queue.toArray();
  if (pending.length === 0) return { applied: 0, skipped: 0, errors: [] };

  const operations = pending.map(({ entity, type, data, client_updated_at }) => ({
    entity,
    type,
    data,
    client_updated_at,
  }));

  const { data: result } = await syncOffline(operations);

  if (result.errors.length === 0) {
    await db.sync_queue.bulkDelete(pending.map((p) => p.localId));
  }

  return result;
}

export async function pendingCount() {
  return db.sync_queue.count();
}
