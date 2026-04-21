import { create } from "zustand";
import type { Dataset } from "../types/datasets";

export interface Feature {
    id: string;
    title: string;
    platform: string;
    acquisitionDate: string;
    productUrl: string;
    dataset: Dataset;
    geometry: {
        type: "Polygon";
        coordinates: [number, number][][];
    };
}

export interface FeaturesState {
    // normalized state
    featuresById: Record<string, Feature>;
    featureIds: string[];

    // actions
    setFeatures: (features: Feature[]) => void;
    addFeatures: (features: Feature[]) => void;
    removeFeature: (id: string) => void;
    clearFeatures: () => void;

    // helpers
    getFeatureById: (id: string) => Feature | undefined;

    // UI state
    hoveredFeatureId: string | null;
    setHoveredFeatureId: (id: string | null) => void;
}

export const useFeaturesStore = create<FeaturesState>((set, get) => ({
    featuresById: {},
    featureIds: [],

    setFeatures: (features) =>
        set({
            featuresById: Object.fromEntries(
                features.map((f) => [f.id, f])
            ),
            featureIds: features.map((f) => f.id),
        }),

    addFeatures: (features) =>
        set((state) => {
            const nextById = { ...state.featuresById };
            const nextIds = [...state.featureIds];

            for (const f of features) {
                nextById[f.id] = f;

                if (!nextIds.includes(f.id)) {
                    nextIds.push(f.id);
                }
            }

            return {
                featuresById: nextById,
                featureIds: nextIds,
            };
        }),

    removeFeature: (id) =>
        set((state) => {
            const { [id]: _, ...rest } = state.featuresById;

            return {
                featuresById: rest,
                featureIds: state.featureIds.filter((fid) => fid !== id),
            };
        }),

    clearFeatures: () =>
        set({
            featuresById: {},
            featureIds: [],
        }),

    getFeatureById: (id) => get().featuresById[id],

    hoveredFeatureId: null,
    setHoveredFeatureId: (id) => set({ hoveredFeatureId: id }),
}));