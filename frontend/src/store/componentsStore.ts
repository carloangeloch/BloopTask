import { create } from "zustand";

type useComponentStoreType = {
  isNavbarOpen: boolean;
  setIsNavbarOpen: (open: boolean) => void;
};

export const useComponentStore = create<useComponentStoreType>((set) => ({
  isNavbarOpen: false,
  setIsNavbarOpen: (open) => set({ isNavbarOpen: open }),
}));
