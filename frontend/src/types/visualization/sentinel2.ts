import type {ButtonOption} from "../../components/sidebar/ButtonGroup.tsx";

export interface Sentinel2BandOption {
    value: string;
    label: string;
}

/**
 * Sentinel-2 available bands for visualization.
 */
export const SENTINEL2_BAND_OPTIONS = [
    {
        value: "1",
        label: "B1 - Coastal Aerosol",
    },
    {
        value: "2",
        label: "B2 - Blue",
    },
    {
        value: "3",
        label: "B3 - Green",
    },
    {
        value: "4",
        label: "B4 - Red",
    },
    {
        value: "5",
        label: "B5 - Vegetation Red Edge",
    },
    {
        value: "6",
        label: "B6 - Vegetation Red Edge",
    },
    {
        value: "7",
        label: "B7 - Vegetation Red Edge",
    },
    {
        value: "8",
        label: "B8 - NIR",
    },
    {
        value: "8A",
        label: "B8A - Narrow NIR",
    },
    {
        value: "9",
        label: "B9 - Water Vapour",
    },
    {
        value: "10",
        label: "B10 - Cirrus",
    },
    {
        value: "11",
        label: "B11 - SWIR 1",
    },
    {
        value: "12",
        label: "B12 - SWIR 2",
    },
    {
        value: "TCI",
        label: "TCI - True Color Image",
    },
] as const satisfies readonly Sentinel2BandOption[];

export type Sentinel2Band = typeof SENTINEL2_BAND_OPTIONS[number]["value"];


/**
 * Bands usable in RGB composites.
 */
export const SENTINEL2_SPECTRAL_BAND_OPTIONS =
    SENTINEL2_BAND_OPTIONS.filter(
        band => band.value !== "TCI"
    );

export type Sentinel2SpectralBand = typeof SENTINEL2_SPECTRAL_BAND_OPTIONS[number]["value"];


/**
 * Visualization mode selected by the user.
 */
export const SENTINEL2_VISUALIZATION_MODE = {
    SINGLE_BANDS: "single-bands",
    CUSTOM_RGB: "custom-rgb",
    PRESETS: "presets",
} as const;

export type Sentinel2VisualizationMode = typeof SENTINEL2_VISUALIZATION_MODE[keyof typeof SENTINEL2_VISUALIZATION_MODE];


/**
 * Supported preset visualization types.
 */
export const SENTINEL2_PRESET_TYPE = {
    RGB_COMPOSITE: "rgb-composite",
    SPECTRAL_INDEX: "spectral-index",
} as const;

export type Sentinel2PresetType = typeof SENTINEL2_PRESET_TYPE[keyof typeof SENTINEL2_PRESET_TYPE];


/**
 * RGB composite.
 */
export interface Sentinel2RGBComposite {
    red: Sentinel2SpectralBand;
    green: Sentinel2SpectralBand;
    blue: Sentinel2SpectralBand;
}


/**
 * Spectral index.
 */
export interface Sentinel2SpectralIndex {
    expression: string;

    min?: number;
    max?: number;

    colorMap?: string;
}


/**
 * Base preset definition.
 */
export interface Sentinel2PresetBase {
    value: string;
    label: string;

    presetType: Sentinel2PresetType;
}


/**
 * RGB preset.
 */
export interface Sentinel2RGBPreset
    extends Sentinel2PresetBase {

    presetType: typeof SENTINEL2_PRESET_TYPE.RGB_COMPOSITE;

    composite: Sentinel2RGBComposite;
}

export const DEFAULT_SENTINEL2_RGB_COMPOSITE: Sentinel2RGBComposite = {
    red: "4",
    green: "3",
    blue: "2",
};


/**
 * Spectral index preset.
 */
export interface Sentinel2SpectralIndexPreset
    extends Sentinel2PresetBase {

    presetType: typeof SENTINEL2_PRESET_TYPE.SPECTRAL_INDEX;

    index: Sentinel2SpectralIndex;
}


/**
 * Any predefined preset.
 */
export type Sentinel2Preset =
    | Sentinel2RGBPreset
    | Sentinel2SpectralIndexPreset;


/**
 * Available presets.
 */
export const SENTINEL2_PRESETS = [
    {
        value: "true-color",
        label: "True Color",

        presetType: SENTINEL2_PRESET_TYPE.RGB_COMPOSITE,

        composite: {
            red: "4",
            green: "3",
            blue: "2",
        },
    },

    {
        value: "false-color-infrared",
        label: "False Color Infrared",

        presetType: SENTINEL2_PRESET_TYPE.RGB_COMPOSITE,

        composite: {
            red: "8",
            green: "4",
            blue: "3",
        },
    },

    {
        value: "agriculture",
        label: "Agriculture",

        presetType: SENTINEL2_PRESET_TYPE.RGB_COMPOSITE,

        composite: {
            red: "11",
            green: "8",
            blue: "2",
        },
    },

    {
        value: "geology",
        label: "Geology",

        presetType: SENTINEL2_PRESET_TYPE.RGB_COMPOSITE,

        composite: {
            red: "12",
            green: "11",
            blue: "2",
        },
    },

    /*
    // zatim jen priprava, asi se bude muset jeste predelat
    {
        value: "ndvi",
        label: "NDVI",

        presetType: SENTINEL2_PRESET_VISUALIZATION.SPECTRAL_INDEX,

        index: {
            expression: "(B08-B04)/(B08+B04)",
            min: -1,
            max: 1,
            colorMap: "ndvi",
        },
    },
    */
] as const satisfies readonly Sentinel2Preset[];

export type Sentinel2PresetId = typeof SENTINEL2_PRESETS[number]["value"];

export const SENTINEL2_PRESET_OPTIONS = SENTINEL2_PRESETS.map(
    ({value, label}) => ({
        value,
        label,
    }),
) satisfies readonly ButtonOption<Sentinel2PresetId>[];