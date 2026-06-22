import { db } from "./schema.js";

export const localFreezerStore = {
  async getAll() {
    const freezers = await db.freezers.toArray();
    for (const f of freezers) {
      f.compartments = await localCompartmentStore.getByFreezer(f.id);
    }
    return freezers;
  },

  async save(freezer) {
    await db.freezers.put(freezer);
  },

  async saveMany(freezers) {
    await db.transaction("rw", db.freezers, db.compartments, db.items, async () => {
      for (const f of freezers) {
        const { compartments, ...fData } = f;
        await db.freezers.put(fData);
        if (compartments) {
          for (const c of compartments) {
            const { items, ...cData } = c;
            await db.compartments.put(cData);
            if (items) await db.items.bulkPut(items);
          }
        }
      }
    });
  },

  async delete(id) {
    await db.freezers.delete(id);
  },
};

export const localCompartmentStore = {
  async getByFreezer(freezer_id) {
    const comps = await db.compartments
      .where("freezer_id").equals(freezer_id)
      .sortBy("position");
    for (const c of comps) {
      c.items = await localItemStore.getByCompartment(c.id);
    }
    return comps;
  },

  async save(comp) {
    await db.compartments.put(comp);
  },

  async delete(id) {
    const items = await db.items.where("compartment_id").equals(id).toArray();
    await db.transaction("rw", db.compartments, db.items, async () => {
      await db.items.bulkDelete(items.map((i) => i.id));
      await db.compartments.delete(id);
    });
  },
};

export const localItemStore = {
  async getByCompartment(compartment_id) {
    return db.items.where("compartment_id").equals(compartment_id).sortBy("name");
  },

  async save(item) {
    await db.items.put(item);
  },

  async delete(id) {
    await db.items.delete(id);
  },
};
