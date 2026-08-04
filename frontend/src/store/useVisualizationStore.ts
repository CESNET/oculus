import {create} from "zustand";

import type {
    ProcessedFileState,
    VisualizationOutput,
} from "../types/visualization";

import {
    DEFAULT_SENTINEL2_RGB_COMPOSITE,
    SENTINEL2_VISUALIZATION_MODE,

    type Sentinel2Band,
    type Sentinel2PresetId,
    type Sentinel2RGBComposite,
    type Sentinel2VisualizationMode,
} from "../types/visualization/sentinel2";


export interface Sentinel1VisualizationState {
    // zatím nic
}


export interface Sentinel2VisualizationState {
    mode: Sentinel2VisualizationMode;

    selectedBands: Sentinel2Band[];
    selectedPresetIds: Sentinel2PresetId[];
    selectedRGBComposite: Sentinel2RGBComposite;
}


const DEFAULT_SENTINEL2_STATE: Sentinel2VisualizationState = {
    mode: SENTINEL2_VISUALIZATION_MODE.SINGLE_BANDS,

    selectedBands: ["TCI"],

    selectedPresetIds: [],

    selectedRGBComposite: DEFAULT_SENTINEL2_RGB_COMPOSITE,
};


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

    setSentinel2(
        partial: Partial<Sentinel2VisualizationState>
    ): void;

    setSentinel2RGBComposite(
        composite: Sentinel2RGBComposite
    ): void;

    toggleSentinel2Band(
        band: Sentinel2Band
    ): void;

    resetSentinel2Bands(
        tci?: boolean
    ): void;

    toggleSentinel2Preset(
        preset: Sentinel2PresetId
    ): void;

    resetSentinel2Presets(): void;

    resetSentinel2RGBComposite(): void;

    resetSentinel2(): void;
}


export const useVisualizationStore =
    create<VisualizationState>((set) => ({

        jobId: null,

        featureId: null,

        sentinel1: {},

        sentinel2: DEFAULT_SENTINEL2_STATE,

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


        setJobId: (jobId) =>
            set({
                jobId,
            }),


        setFeatureId: (featureId) =>
            set({
                featureId,
            }),


        setProcessedFiles: (processedFiles) =>
            set({
                processedFiles,
            }),


        setOutputs: (outputs) =>
            set({
                outputs,
            }),


        setSelectedTileLayerPath: (selectedTileLayerPath) =>
            set({
                selectedTileLayerPath,
            }),


        setOpacity: (opacity) =>
            set({
                opacity,
            }),


        setSentinel2: (partial) =>
            set((state) => ({
                sentinel2: {
                    ...state.sentinel2,
                    ...partial,
                },
            })),


        setSentinel2RGBComposite: (selectedRGBComposite) =>
            set((state) => ({
                sentinel2: {
                    ...state.sentinel2,
                    selectedRGBComposite,
                },
            })),


        toggleSentinel2Band: (band) =>
            set((state) => ({
                sentinel2: {
                    ...state.sentinel2,

                    selectedBands:
                        state.sentinel2.selectedBands.includes(band)
                            ? state.sentinel2.selectedBands.filter(
                                (b) => b !== band
                            )
                            : [
                                ...state.sentinel2.selectedBands,
                                band,
                            ],
                },
            })),


        resetSentinel2Bands: (tci = false) =>
            set((state) => ({
                sentinel2: {
                    ...state.sentinel2,

                    selectedBands: tci
                        ? ["TCI"]
                        : [],
                },
            })),


        toggleSentinel2Preset: (preset) =>
            set((state) => ({
                sentinel2: {
                    ...state.sentinel2,

                    selectedPresetIds:
                        state.sentinel2.selectedPresetIds.includes(
                            preset
                        )
                            ? state.sentinel2.selectedPresetIds.filter(
                                (p) => p !== preset
                            )
                            : [
                                ...state.sentinel2.selectedPresetIds,
                                preset,
                            ],
                },
            })),


        resetSentinel2Presets: () =>
            set((state) => ({
                sentinel2: {
                    ...state.sentinel2,

                    selectedPresetIds: [],
                },
            })),


        resetSentinel2RGBComposite: () =>
            set((state) => ({
                sentinel2: {
                    ...state.sentinel2,

                    selectedRGBComposite:
                    DEFAULT_SENTINEL2_RGB_COMPOSITE,
                },
            })),


        resetSentinel2: () =>
            set({
                sentinel2: DEFAULT_SENTINEL2_STATE,
            }),
    }));