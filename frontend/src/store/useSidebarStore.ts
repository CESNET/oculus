import {create} from "zustand";

interface SidebarState {
    activeTab: number;
    setActiveTab: (i: number) => void;
}

export const useSidebarStore = create<SidebarState>((set) => ({
    activeTab: 0,
    setActiveTab: (i) => set({activeTab: i}),
}));
