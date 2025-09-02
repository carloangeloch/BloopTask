import { create } from "zustand";

type useTeamStoreType = {
  activeTeam: number;
  setActiveTeam: (team: number) => void;
};

export const useTeamStore = create<useTeamStoreType>((set) => ({
  activeTeam: 0,
  setActiveTeam: (team) => set({ activeTeam: team }),
}));
