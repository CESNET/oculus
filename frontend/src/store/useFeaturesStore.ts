import {create} from "zustand";

export interface Feature {
    id: string;
    title: string;
    platform: string;
    acquisitionDate: string;
    productUrl: string;
}

export interface FeaturesState {
    features: Feature[];
    setFeatures: (features: Feature[]) => void;
    addFeatures: (features: Feature[]) => void;
    clearFeatures: () => void;
}

export const useFeaturesStore = create<FeaturesState>((set) => ({
    features: [],
    setFeatures: (features) => set({features}),
    addFeatures: (features) => set((state) => ({features: [...state.features, ...features]})),
    clearFeatures: () => set({features: []}),
}));
