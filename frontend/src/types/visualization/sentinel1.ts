import type {ButtonOption} from "../../components/sidebar/ButtonGroup.tsx";


// ======================================================
// POLARIZATIONS
// ======================================================

export interface Sentinel1PolarizationDefinition {
    id: string;
    label: string;
}


export const SENTINEL1_POLARIZATIONS = [
    {
        id: "VV",
        label: "VV - Vertical transmit / Vertical receive",
    },
    {
        id: "VH",
        label: "VH - Vertical transmit / Horizontal receive",
    },
    {
        id: "HH",
        label: "HH - Horizontal transmit / Horizontal receive",
    },
    {
        id: "HV",
        label: "HV - Horizontal transmit / Vertical receive",
    },
] as const satisfies readonly Sentinel1PolarizationDefinition[];


export type Sentinel1Polarization = typeof SENTINEL1_POLARIZATIONS[number]["id"];


// UI adapter

export const SENTINEL1_POLARIZATION_OPTIONS =
    SENTINEL1_POLARIZATIONS.map(
        polarization => ({
            value: polarization.id,
            label: polarization.label,
        }),
    ) satisfies readonly ButtonOption<Sentinel1Polarization>[];


// ======================================================
// VISUALIZATION MODE
// ======================================================

export const SENTINEL1_VISUALIZATION_MODE = {
    POLARIZATIONS: "polarizations",
    PRESETS: "presets",
} as const;


export type Sentinel1VisualizationMode = typeof SENTINEL1_VISUALIZATION_MODE[        keyof typeof SENTINEL1_VISUALIZATION_MODE        ];


// ======================================================
// PRESETS
// ======================================================

export interface Sentinel1Preset {
    id: string;
    label: string;
    polarization: Sentinel1Polarization;
}


export const SENTINEL1_PRESETS = [
    {
        id: "vv",
        label: "VV",
        polarization: "VV",
    },
    {
        id: "vh",
        label: "VH",
        polarization: "VH",
    },
    {
        id: "hh",
        label: "HH",
        polarization: "HH",
    },
    {
        id: "hv",
        label: "HV",
        polarization: "HV",
    },
] as const satisfies readonly Sentinel1Preset[];


export type Sentinel1PresetId = typeof SENTINEL1_PRESETS[number]["id"];


// UI adapter

export const SENTINEL1_PRESET_OPTIONS =
    SENTINEL1_PRESETS.map(
        preset => ({
            value: preset.id,
            label: preset.label,
        }),
    ) satisfies readonly ButtonOption<Sentinel1PresetId>[];


// ======================================================
// BACKEND PAYLOAD TYPES
// ======================================================

export interface Sentinel1Visualizations {
    /**
     * Individual polarizations to generate.
     *
     * Example:
     * ["VV", "VH"]
     */
    polarizations?: Sentinel1Polarization[];

    /**
     * Named presets.
     */
    presets?: Sentinel1PresetId[];
}