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

interface VisualizationState {
    jobId: string | null;
    featureId: string | null;
    outputs: Record<string, { full_product: boolean; wm_tiles: boolean }>;
    processedFiles: ProductFile[];
    tileLayers: TileLayer[];
    availableZoomLevels: number[];
    selectedTileLayerIndex: number | null;
    opacity: number; // globální pro vybraný tileLayer (0..1)

    setJobId: (id: string | null) => void;
    setFeatureId: (id: string | null) => void;
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
    setOutputs: (outputs) => set({outputs}),
    setProcessedFiles: (files) => set({processedFiles: files}),
    setTileLayers: (tiles) => set({tileLayers: tiles}),
    setAvailableZoomLevels: (availableZoomLevels) => set({availableZoomLevels: availableZoomLevels}),
    setSelectedTileLayerIndex: (index) => set({selectedTileLayerIndex: index}),
    setOpacity: (opacity) => set({opacity})
}));