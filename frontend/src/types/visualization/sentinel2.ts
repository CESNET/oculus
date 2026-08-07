import type {ButtonOption} from "../../components/sidebar/ButtonGroup.tsx";

/**
 * Sentinel-2 available band definition.
 */
export interface Sentinel2BandDefinition {
    id: string;
    label: string;
}


/**
 * Sentinel-2 available bands.
 */
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

export const SENTINEL2_BAND_OPTIONS =
    SENTINEL2_BANDS.map(
        band => ({
            value: band.id,
            label: band.label,
        }),
    );

/**
 * Bands usable in RGB composites.
 */
export const SENTINEL2_SPECTRAL_BANDS =
    SENTINEL2_BANDS.filter(band => band.id !== "TCI");

export type Sentinel2SpectralBand = typeof SENTINEL2_SPECTRAL_BANDS[number]["id"];

export const SENTINEL2_SPECTRAL_BAND_OPTIONS =
    SENTINEL2_SPECTRAL_BANDS.map(
        band => ({
            value: band.id,
            label: band.label,
        }),
    );

/**
 * Visualization mode selected in UI.
 */
export const SENTINEL2_VISUALIZATION_MODE = {
    SINGLE_BANDS: "single-bands",
    CUSTOM_RGB: "custom-rgb",
    PRESETS: "presets",
} as const;

export type Sentinel2VisualizationMode = typeof SENTINEL2_VISUALIZATION_MODE[keyof typeof SENTINEL2_VISUALIZATION_MODE];


/**
 * Preset types.
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

export const DEFAULT_SENTINEL2_RGB_COMPOSITE: Sentinel2RGBComposite = {
    red: "4",
    green: "3",
    blue: "2",
};


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
 * Base preset.
 */
export interface Sentinel2PresetBase {
    id: string;
    label: string;

    presetType: Sentinel2PresetType;
}


/**
 * RGB preset.
 */
export interface Sentinel2RGBPreset extends Sentinel2PresetBase {
    presetType: typeof SENTINEL2_PRESET_TYPE.RGB_COMPOSITE;
    composite: Sentinel2RGBComposite;
}


/**
 * Spectral index preset.
 */
export interface Sentinel2SpectralIndexPreset extends Sentinel2PresetBase {
    presetType: typeof SENTINEL2_PRESET_TYPE.SPECTRAL_INDEX;
    index: Sentinel2SpectralIndex;
}


/**
 * Any preset.
 */
export type Sentinel2Preset = | Sentinel2RGBPreset | Sentinel2SpectralIndexPreset;

/**
 * Available presets.
 */
export const SENTINEL2_PRESETS = [
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

    /*
    {
        id: "ndvi",
        label: "NDVI",

        presetType: SENTINEL2_PRESET_TYPE.SPECTRAL_INDEX,

        index: {
            expression: "(B08-B04)/(B08+B04)",
            min: -1,
            max: 1,
            colorMap: "ndvi",
        },
    },
    */
] as const satisfies readonly Sentinel2Preset[];

export type Sentinel2PresetId = typeof SENTINEL2_PRESETS[number]["id"];


/**
 * Button options.
 */
export const SENTINEL2_PRESET_OPTIONS = SENTINEL2_PRESETS.map(
    ({id, label}) => ({
        value: id,
        label,
    }),
) satisfies readonly ButtonOption<Sentinel2PresetId>[];


/**
 * Payload sent to backend.
 */
export interface Sentinel2Visualizations {
    bands?: Sentinel2Band[];
    rgb?: Sentinel2RGBComposite;
    presets?: Sentinel2PresetId[];
}