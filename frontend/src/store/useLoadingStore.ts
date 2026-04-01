import { create } from "zustand";

interface LoadingState {
    isLoading: boolean;
    abortController: AbortController | null;
    startLoading: () => AbortController;
    stopLoading: () => void;
}

export const useLoadingStore = create<LoadingState>((set, get) => ({
    isLoading: false,
    abortController: null,

    startLoading: () => {
        const controller = new AbortController();
        set({ isLoading: true, abortController: controller });
        return controller;
    },

    stopLoading: () => {
        const { abortController } = get();
        if (abortController) {
            abortController.abort(); // Zruší probíhající fetch
        }
        set({ isLoading: false, abortController: null });
    }
}));
