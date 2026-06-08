import { create } from "zustand";
import { persist } from "zustand/middleware";

interface ProductsState {
  selectedIds: number[];
  toggle: (id: number) => void;
  selectAll: (ids: number[]) => void;
  clearAll: () => void;
}

export const useProductsStore = create<ProductsState>()(
  persist(
    (set) => ({
      selectedIds: [],
      toggle: (id) =>
        set((s) =>
          s.selectedIds.includes(id)
            ? { selectedIds: s.selectedIds.filter((x) => x !== id) }
            : { selectedIds: [...s.selectedIds, id] }
        ),
      selectAll: (ids) => set({ selectedIds: ids }),
      clearAll: () => set({ selectedIds: [] }),
    }),
    { name: "selected-products" }
  )
);
