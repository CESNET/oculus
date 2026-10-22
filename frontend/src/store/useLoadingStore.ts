
import { create } from "zustand";
import { LoadingType } from "../types/loadingTypes";

interface LoadingState {
    isLoading: boolean;
    loadingType: LoadingType;
    abortController: AbortController | null;

    startLoading: (type?: LoadingType) => AbortController;
    finishLoading: (controller: AbortController) => void;
    stopLoading: () => void;
}

export const useLoadingStore = create<LoadingState>((set, get) => ({
    isLoading: false,
    loadingType: LoadingType.DEFAULT,
    abortController: null,

    startLoading: (type = LoadingType.DEFAULT) => {
        get().abortController?.abort();

        const controller = new AbortController();

        set({
            isLoading: true,
            loadingType: type,
            abortController: controller,
        });

        return controller;
    },

    finishLoading: (controller) => {
        if (get().abortController !== controller) return;

        set({
            isLoading: false,
            loadingType: LoadingType.DEFAULT,
            abortController: null,
        });
    },

    stopLoading: () => {
        const controller = get().abortController;

        set({
            isLoading: false,
            loadingType: LoadingType.DEFAULT,
            abortController: null,
        });

        controller?.abort();
    },
}));
