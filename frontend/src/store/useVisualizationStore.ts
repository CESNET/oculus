import {create} from "zustand";
import type {
    ProcessedFileState,
    VisualizationOutput
} from "../types/visualization";

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

    /**
     * Original response from backend
     */
    processedFiles: Record<string, ProcessedFileState>;

    /**
     * Requested outputs
     */
    outputs: Record<string, VisualizationOutput>;

    /**
     * Currently displayed WM tile layer
     */
    selectedTileLayerPath: string | null;

    opacity: number;


    setJobId(id: string | null): void;

    setFeatureId(id: string | null): void;

    setProcessedFiles(files: Record<string, ProcessedFileState>): void;

    setOutputs(outputs: Record<string, VisualizationOutput>): void;

    setSelectedTileLayerPath(path: string | null): void;

    setOpacity(opacity: number): void;

    setSentinel2(partial: Partial<Sentinel2VisualizationState>): void;

    toggleSentinel2Band(band: string): void;

    resetSentinel2Bands(tci?: boolean): void;
}


export const useVisualizationStore =
    create<VisualizationState>((set) => ({
        jobId: null,
        featureId: null,

        sentinel1: {},

        sentinel2: {
            bands: ["TCI"],
        },

        processedFiles: {},

        outputs: {
            jpg: {
                full_product: true,
                wm_tiles: false,
            },

            png: {
                full_product: false,
                wm_tiles: false,
            },

            webp: {
                full_product: false,
                wm_tiles: true,
            },
        },

        selectedTileLayerPath: null,

        opacity: 0.8,

        setJobId: (id) => set({
            jobId: id,
        }),

        setFeatureId: (id) => set({
            featureId: id,
        }),

        setProcessedFiles: (files) => set({
            processedFiles: files,
        }),

        setOutputs: (outputs) => set({
            outputs,
        }),

        setSelectedTileLayerPath: (path) => set({
            selectedTileLayerPath: path,
        }),

        setOpacity: (opacity) => set({
            opacity,
        }),


        setSentinel2: (partial) => set((state) => ({
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
                        ? state.sentinel2.bands.filter(
                            b => b !== band
                        )
                        : [
                            ...state.sentinel2.bands,
                            band
                        ],
                },
            })),

        resetSentinel2Bands: (tci = false) =>
            set((state) => ({
                sentinel2: {
                    ...state.sentinel2,

                    bands: tci
                        ? ["TCI"]
                        : [],
                },
            })),
    }));
