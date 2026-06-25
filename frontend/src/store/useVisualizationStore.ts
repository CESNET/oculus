import {create} from "zustand";

export interface ProductFile {
    path: string;
    name: string; // s příponou
    format: string;
}

export interface TileLayer {
    path: string; // složka s dlaždicemi
    name: string; // bez přípony, pro select
    format: string; // webp, jpg, ...
}

export interface Sentinel1VisualizationState {
    // zatím nic
}

export interface Sentinel2VisualizationState {
    bands: string[];
}


interface VisualizationState {
    jobId: string | null;
    featureId: string | null;

    sentinel1: Sentinel1VisualizationState;
    sentinel2: Sentinel2VisualizationState;

    outputs: Record<string, { full_product: boolean; wm_tiles: boolean }>;
    processedFiles: ProductFile[];
    tileLayers: TileLayer[];
    availableZoomLevels: number[];
    selectedTileLayerIndex: number | null;
    opacity: number; // globální pro vybraný tileLayer (0..1)


    setJobId: (id: string | null) => void;
    setFeatureId: (id: string | null) => void;

    setSentinel2: (
        partial: Partial<Sentinel2VisualizationState>
    ) => void;
    toggleSentinel2Band: (band: string) => void;
    resetSentinel2Bands: (tci?: boolean) => void;

    setOutputs: (outputs: Record<string, { full_product: boolean; wm_tiles: boolean }>) => void;
    setProcessedFiles: (files: ProductFile[]) => void;
    setTileLayers: (tiles: TileLayer[]) => void;
    setAvailableZoomLevels: (availableZoomLevels: number[]) => void;
    setSelectedTileLayerIndex: (index: number | null) => void;
    setOpacity: (opacity: number) => void;
}

export const useVisualizationStore = create<VisualizationState>((set) => ({
    jobId: null,
    featureId: null,

    sentinel1: {},

    sentinel2: {
        bands: ["TCI"],
    },

    outputs: {
        jpg: {full_product: true, wm_tiles: false},
        png: {full_product: false, wm_tiles: false},
        webp: {full_product: false, wm_tiles: true}
    },
    processedFiles: [],
    tileLayers: [],
    availableZoomLevels: [],
    selectedTileLayerIndex: null,
    opacity: 0.8,

    setJobId: (id) => set({jobId: id}),
    setFeatureId: (id) => set({featureId: id}),

    setSentinel2: (partial) =>
        set((state) => ({
            sentinel2: {
                ...state.sentinel2,
                ...partial,
            },
        })),

    toggleSentinel2Band: (band) =>
        set((state) => ({
            sentinel2: {
                ...state.sentinel2,
                bands: state.sentinel2.bands.includes(band)
                    ? state.sentinel2.bands.filter((b) => b !== band)
                    : [...state.sentinel2.bands, band],
            },
        })),

    resetSentinel2Bands: (tci?: boolean) =>
        set((state) => ({
            sentinel2: {
                ...state.sentinel2,
                bands: tci ? ["TCI"] : [],
            },
        })),

    setOutputs: (outputs) => set({outputs}),
    setProcessedFiles: (files) => set({processedFiles: files}),
    setTileLayers: (tiles) => set({tileLayers: tiles}),
    setAvailableZoomLevels: (availableZoomLevels) => set({availableZoomLevels: availableZoomLevels}),
    setSelectedTileLayerIndex: (index) => set({selectedTileLayerIndex: index}),
    setOpacity: (opacity) => set({opacity})
}));