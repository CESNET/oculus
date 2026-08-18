import type {ButtonOption} from "../../components/sidebar/ButtonGroup.tsx";


// ======================================================
// BANDS
// ======================================================

export interface Sentinel2BandDefinition {
    id: string;
    label: string;
}


export const SENTINEL2_BANDS = [
    {
        id: "1",
        label: "B1 - Coastal Aerosol",
    },
    {
        id: "2",
        label: "B2 - Blue",
    },
    {
        id: "3",
        label: "B3 - Green",
    },
    {
        id: "4",
        label: "B4 - Red",
    },
    {
        id: "5",
        label: "B5 - Vegetation Red Edge",
    },
    {
        id: "6",
        label: "B6 - Vegetation Red Edge",
    },
    {
        id: "7",
        label: "B7 - Vegetation Red Edge",
    },
    {
        id: "8",
        label: "B8 - NIR",
    },
    {
        id: "8A",
        label: "B8A - Narrow NIR",
    },
    {
        id: "9",
        label: "B9 - Water Vapour",
    },
    {
        id: "10",
        label: "B10 - Cirrus",
    },
    {
        id: "11",
        label: "B11 - SWIR 1",
    },
    {
        id: "12",
        label: "B12 - SWIR 2",
    },
    {
        id: "TCI",
        label: "TCI - True Color Image",
    },
] as const satisfies readonly Sentinel2BandDefinition[];


export type Sentinel2Band = typeof SENTINEL2_BANDS[number]["id"];


// UI adapter

export const SENTINEL2_BAND_OPTIONS = SENTINEL2_BANDS.map(
    band => ({
        value: band.id,
        label: band.label,
    }),
) satisfies readonly ButtonOption<Sentinel2Band>[];


// ======================================================
// SPECTRAL BANDS
// ======================================================

export const SENTINEL2_SPECTRAL_BANDS = SENTINEL2_BANDS.filter(
    band => band.id !== "TCI",
);


export type Sentinel2SpectralBand = typeof SENTINEL2_SPECTRAL_BANDS[number]["id"];


export const SENTINEL2_SPECTRAL_BAND_OPTIONS = SENTINEL2_SPECTRAL_BANDS.map(
    band => ({
        value: band.id,
        label: band.label,
    }),
) satisfies readonly ButtonOption<Sentinel2SpectralBand>[];


// ======================================================
// VISUALIZATION MODE
// ======================================================

export const SENTINEL2_VISUALIZATION_MODE = {
    SINGLE_BANDS: "single-bands",
    CUSTOM_RGB: "custom-rgb",
    PRESETS: "presets",
} as const;


export type Sentinel2VisualizationMode = typeof SENTINEL2_VISUALIZATION_MODE[keyof typeof SENTINEL2_VISUALIZATION_MODE];


// ======================================================
// RGB COMPOSITE
// ======================================================

export interface Sentinel2RGBComposite {
    red: Sentinel2SpectralBand;
    green: Sentinel2SpectralBand;
    blue: Sentinel2SpectralBand;
}


export const DEFAULT_SENTINEL2_RGB_COMPOSITE: Sentinel2RGBComposite = {
    red: "4",
    green: "3",
    blue: "2",
};


// ======================================================
// FEATURES / SPECTRAL INDICES
// ======================================================

export const SENTINEL2_INDEX = {
    HONS: "HONS",
    NDVI: "NDVI",
    NDWI: "NDWI",
    NDMI: "NDMI",
    NDSI: "NDSI",
    ND_UNSPEC: "ND_UNSPEC",
} as const;


export type Sentinel2Index = typeof SENTINEL2_INDEX[keyof typeof SENTINEL2_INDEX];


// ======================================================
// REQUIRED BANDS FOR FIXED FEATURES
// ======================================================

/**
 * Required input bands for features with a fixed definition.
 *
 * The order is important because it corresponds to the order
 * expected by gjtiff:
 *
 * HONS      -> B04, B03, B02
 * NDVI      -> B08, B04
 * NDWI      -> B03, B08
 * NDMI      -> B8A, B11
 * NDSI      -> B03, B11, B04, B02
 */
export const SENTINEL2_INDEX_BANDS = {
    [SENTINEL2_INDEX.HONS]: ["4", "3", "2"],
    [SENTINEL2_INDEX.NDVI]: ["8", "4"],
    [SENTINEL2_INDEX.NDWI]: ["3", "8"],
    [SENTINEL2_INDEX.NDMI]: ["8A", "11"],
    [SENTINEL2_INDEX.NDSI]: ["3", "11", "4", "2"],
} as const satisfies Record<
    Exclude<Sentinel2Index, typeof SENTINEL2_INDEX.ND_UNSPEC>,
    readonly Sentinel2SpectralBand[]
>;


// ======================================================
// CUSTOM NORMALIZED DIFFERENCE
// ======================================================

/**
 * Generic normalized difference:
 *
 *     (Bx - By) / (Bx + By)
 *
 * Unlike the fixed spectral indices, the user chooses
 * both input bands.
 */
export interface Sentinel2CustomNormalizedDifference {
    band1: Sentinel2SpectralBand;
    band2: Sentinel2SpectralBand;
}


// ======================================================
// INDEX VISUALIZATION
// ======================================================

export interface Sentinel2IndexVisualization {
    index: Sentinel2Index;

    /**
     * Only used for ND_UNSPEC.
     */
    band1?: Sentinel2SpectralBand;
    band2?: Sentinel2SpectralBand;
}


// ======================================================
// PRESETS
// ======================================================

export const SENTINEL2_PRESET_TYPE = {
    RGB_COMPOSITE: "rgb-composite",
    INDEX: "index",
} as const;


export type Sentinel2PresetType = typeof SENTINEL2_PRESET_TYPE[keyof typeof SENTINEL2_PRESET_TYPE];


export interface Sentinel2PresetBase {
    id: string;
    label: string;
    presetType: Sentinel2PresetType;
}


export interface Sentinel2RGBPreset extends Sentinel2PresetBase {
    presetType: typeof SENTINEL2_PRESET_TYPE.RGB_COMPOSITE;
    composite: Sentinel2RGBComposite;
}


export interface Sentinel2IndexPreset extends Sentinel2PresetBase {
    presetType: typeof SENTINEL2_PRESET_TYPE.INDEX;
    index: Sentinel2Index;
}


export type Sentinel2Preset = Sentinel2RGBPreset | Sentinel2IndexPreset;


// ======================================================
// PRESET DEFINITIONS
// ======================================================

export const SENTINEL2_PRESETS = [
    // --------------------------------------------------
    // RGB composites
    // --------------------------------------------------

    {
        id: "true-color",
        label: "True Color",

        presetType: SENTINEL2_PRESET_TYPE.RGB_COMPOSITE,

        composite: {
            red: "4",
            green: "3",
            blue: "2",
        },
    },

    {
        id: "false-color-infrared",
        label: "False Color Infrared",

        presetType: SENTINEL2_PRESET_TYPE.RGB_COMPOSITE,

        composite: {
            red: "8",
            green: "4",
            blue: "3",
        },
    },

    {
        id: "agriculture",
        label: "Agriculture",

        presetType: SENTINEL2_PRESET_TYPE.RGB_COMPOSITE,

        composite: {
            red: "11",
            green: "8",
            blue: "2",
        },
    },

    {
        id: "geology",
        label: "Geology",

        presetType: SENTINEL2_PRESET_TYPE.RGB_COMPOSITE,

        composite: {
            red: "12",
            green: "11",
            blue: "2",
        },
    },

    // --------------------------------------------------
    // Spectral / combined features
    // --------------------------------------------------

    {
        id: "hons",
        label: "HONS",

        presetType: SENTINEL2_PRESET_TYPE.INDEX,

        index: SENTINEL2_INDEX.HONS,
    },

    {
        id: "ndvi",
        label: "NDVI",

        presetType: SENTINEL2_PRESET_TYPE.INDEX,

        index: SENTINEL2_INDEX.NDVI,
    },

    {
        id: "ndwi",
        label: "NDWI",

        presetType: SENTINEL2_PRESET_TYPE.INDEX,

        index: SENTINEL2_INDEX.NDWI,
    },

    {
        id: "ndmi",
        label: "NDMI",

        presetType: SENTINEL2_PRESET_TYPE.INDEX,

        index: SENTINEL2_INDEX.NDMI,
    },

    {
        id: "ndsi",
        label: "NDSI",

        presetType: SENTINEL2_PRESET_TYPE.INDEX,

        index: SENTINEL2_INDEX.NDSI,
    },
] as const satisfies readonly Sentinel2Preset[];


export type Sentinel2PresetId = typeof SENTINEL2_PRESETS[number]["id"];


// UI adapter

export const SENTINEL2_PRESET_OPTIONS =
    SENTINEL2_PRESETS.map(
        preset => ({
            value: preset.id,
            label: preset.label,
        }),
    ) satisfies readonly ButtonOption<Sentinel2PresetId>[];


// ======================================================
// BACKEND PAYLOAD TYPES
// ======================================================

export interface Sentinel2RGBVisualization {
    red: Sentinel2SpectralBand;
    green: Sentinel2SpectralBand;
    blue: Sentinel2SpectralBand;
}


export interface Sentinel2Visualizations {
    /**
     * Individual bands to generate.
     *
     * Example:
     * ["4", "8", "11"]
     */
    bands?: Sentinel2SpectralBand[];

    /**
     * Custom RGB composite.
     *
     * Example:
     * {
     *     red: "8",
     *     green: "4",
     *     blue: "3"
     * }
     */
    rgb?: Sentinel2RGBVisualization;

    /**
     * Spectral / combined features.
     *
     * Fixed features:
     *     { feature: "NDVI" }
     *     { feature: "NDWI" }
     *     { feature: "NDMI" }
     *     { feature: "NDSI" }
     *     { feature: "HONS" }
     *
     * Custom:
     *     {
     *         feature: "ND_UNSPEC",
     *         band1: "8",
     *         band2: "4"
     *     }
     */
    features?: Sentinel2IndexVisualization[];

    /**
     * Named presets.
     */
    presets?: Sentinel2PresetId[];
}
