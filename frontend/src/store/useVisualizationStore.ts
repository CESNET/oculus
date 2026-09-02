import {create} from "zustand";

import type {
    ProcessedFileState,
    VisualizationRequestOutput,
} from "../types/visualization";

import {
    DEFAULT_SENTINEL2_RGB_COMPOSITE,
    SENTINEL2_VISUALIZATION_MODE,

    type Sentinel2Band,
    type Sentinel2PresetId,
    type Sentinel2RGBComposite,
    type Sentinel2VisualizationMode,
} from "../types/visualization/sentinel2";


// ======================================================
// DATASET VISUALIZATION STATE
// ======================================================

export interface Sentinel1VisualizationState {
    // zatím nic
}


export interface Sentinel2VisualizationState {
    /**
     * UI only.
     */
    mode: Sentinel2VisualizationMode;

    /**
     * Individual bands to generate.
     */
    selectedBands: Sentinel2Band[];

    /**
     * Presets to generate.
     */
    selectedPresetIds: Sentinel2PresetId[];

    /**
     * Generate custom RGB composite.
     */
    generateRGB: boolean;

    /**
     * RGB composite definition.
     */
    selectedRGBComposite: Sentinel2RGBComposite;
}


export interface LandsatVisualizationState {
    // TODO: with Landsat implementation
}


// ======================================================
// DEFAULT STATE
// ======================================================

const DEFAULT_SENTINEL2_STATE: Sentinel2VisualizationState = {
    mode: SENTINEL2_VISUALIZATION_MODE.SINGLE_BANDS,

    selectedBands: ["TCI"],

    selectedPresetIds: [],

    generateRGB: false,

    selectedRGBComposite: DEFAULT_SENTINEL2_RGB_COMPOSITE,
};


// ======================================================
// STORE
// ======================================================

export interface VisualizationState {
    // --------------------------------------------------
    // Job
    // --------------------------------------------------

    jobId: string | null;

    featureId: string | null;


    // --------------------------------------------------
    // Dataset-specific visualization settings
    // --------------------------------------------------

    sentinel1: Sentinel1VisualizationState;

    sentinel2: Sentinel2VisualizationState;

    landsat: LandsatVisualizationState;


    // --------------------------------------------------
    // Request output configuration
    // --------------------------------------------------

    /**
     * Output formats requested from the backend.
     *
     * Example:
     *
     * {
     *     jpg: {
     *         full_product: true,
     *         wm_tiles: false,
     *     },
     *     webp: {
     *         full_product: false,
     *         wm_tiles: true,
     *     },
     * }
     */
    outputs: Record<string, VisualizationRequestOutput>;


    // --------------------------------------------------
    // Processing results
    // --------------------------------------------------

    /**
     * Actual visualization outputs returned by the backend.
     *
     * Key = visualization ID, e.g.:
     *   "TCI"
     *   "B02"
     *   "rgb_B04-B8A-B11"
     *   "ndvi_B08-B04"
     */
    processedFiles: Record<string, ProcessedFileState>;


    // --------------------------------------------------
    // Map
    // --------------------------------------------------

    selectedTileLayerPath: string | null;

    opacity: number;


    // --------------------------------------------------
    // Generic setters
    // --------------------------------------------------

    setJobId(
        id: string | null
    ): void;

    setFeatureId(
        id: string | null
    ): void;

    setOutputs(
        outputs: Record<string, VisualizationRequestOutput>
    ): void;

    setProcessedFiles(
        files: Record<string, ProcessedFileState>
    ): void;

    setSelectedTileLayerPath(
        path: string | null
    ): void;

    setOpacity(
        opacity: number
    ): void;


    // --------------------------------------------------
    // Sentinel-2 setters
    // --------------------------------------------------

    setSentinel2(
        partial: Partial<Sentinel2VisualizationState>
    ): void;

    setGenerateSentinel2RGB(
        enabled: boolean
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

        // ==================================================
        // INITIAL STATE
        // ==================================================

        jobId: null,

        featureId: null,


        // --------------------------------------------------
        // Dataset state
        // --------------------------------------------------

        sentinel1: {},

        sentinel2: DEFAULT_SENTINEL2_STATE,

        landsat: {},


        // --------------------------------------------------
        // Request output configuration
        // --------------------------------------------------

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


        // --------------------------------------------------
        // Processing results
        // --------------------------------------------------

        processedFiles: {},


        // --------------------------------------------------
        // Map
        // --------------------------------------------------

        selectedTileLayerPath: null,

        opacity: 0.8,


        // ==================================================
        // GENERIC SETTERS
        // ==================================================

        setJobId: (jobId) =>
            set({
                jobId,
            }),

        setFeatureId: (featureId) =>
            set({
                featureId,
            }),

        setOutputs: (outputs) =>
            set({
                outputs,
            }),

        setProcessedFiles: (processedFiles) =>
            set({
                processedFiles,
            }),

        setSelectedTileLayerPath: (selectedTileLayerPath) =>
            set({
                selectedTileLayerPath,
            }),

        setOpacity: (opacity) =>
            set({
                opacity,
            }),


        // ==================================================
        // SENTINEL-2
        // ==================================================

        setSentinel2: (partial) =>
            set((state) => ({
                sentinel2: {
                    ...state.sentinel2,
                    ...partial,
                },
            })),

        setGenerateSentinel2RGB: (generateRGB) =>
            set((state) => ({
                sentinel2: {
                    ...state.sentinel2,
                    generateRGB,
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
                                b => b !== band
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

                    selectedBands: tci ? ["TCI"] : [],
                },
            })),

        toggleSentinel2Preset: (preset) =>
            set((state) => ({
                sentinel2: {
                    ...state.sentinel2,

                    selectedPresetIds:
                        state.sentinel2.selectedPresetIds.includes(preset)
                            ? state.sentinel2.selectedPresetIds.filter(
                                p => p !== preset
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

                    generateRGB: false,

                    selectedRGBComposite:
                    DEFAULT_SENTINEL2_RGB_COMPOSITE,
                },
            })),

        resetSentinel2: () =>
            set({
                sentinel2: {
                    ...DEFAULT_SENTINEL2_STATE,

                    selectedBands: [
                        ...DEFAULT_SENTINEL2_STATE.selectedBands,
                    ],

                    selectedPresetIds: [
                        ...DEFAULT_SENTINEL2_STATE.selectedPresetIds,
                    ],
                },
            }),
    }));