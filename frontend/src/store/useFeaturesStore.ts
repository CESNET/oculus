import { create } from "zustand";

export interface Feature {
    id: string;
    title: string;
    platform: string;
    acquisitionDate: string;
    productUrl: string;
    geometry: {
        type: "Polygon";
        coordinates: [number, number][][]; // [lat, lng] pro mapové knihovny
    };
}

export interface FeaturesState {
    features: Feature[];
    setFeatures: (features: Feature[]) => void;
    addFeatures: (features: Feature[]) => void;
    clearFeatures: () => void;

    hoveredFeatureId: string | null;
    setHoveredFeatureId: (id: string | null) => void;
}

export const useFeaturesStore = create<FeaturesState>((set) => ({
    features: [],
    setFeatures: (features) => set({ features }),
    addFeatures: (features) => set((state) => ({
        features: [...state.features, ...features]
    })),
    clearFeatures: () => set({ features: [] }),

    hoveredFeatureId: null,
    setHoveredFeatureId: (id) => set({ hoveredFeatureId: id }),
}));