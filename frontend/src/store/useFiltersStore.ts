import { create } from "zustand";
import { Dataset } from "../types/datasets";

// -----------------------------
// Typy
// -----------------------------
export interface BoundingBox {
    north: number;
    south: number;
    east: number;
    west: number;
}

export interface Datetime {
    start: string;
    end: string;
}

export interface Sentinel1FilterState {
    levels: string[];
    sensingTypes: string[];
    productTypes: string[];
    polarizations: string[];
}

export interface Sentinel2FilterState {
    cloudCover: number | null;
    levels: string[];
    bands: string[];
}

export interface FiltersState {
    dataset: Dataset;
    setDataset: (d: Dataset) => void;

    bbox: BoundingBox;
    datetime: Datetime;

    sentinel1: Sentinel1FilterState;
    sentinel2: Sentinel2FilterState;

    setFilters: (filters: Partial<FiltersState>) => void;

    // bbox + datetime
    setBbox: (bbox: Partial<BoundingBox>) => void;
    setBboxFromMap: (n: number, s: number, e: number, w: number) => void;
    setDatetime: (datetime: Partial<{ start: string; end: string }>) => void;

    // sentinel1
    toggleSentinel1: (
        key: keyof Sentinel1FilterState,
        value: string
    ) => void;

    // sentinel2
    setSentinel2: (partial: Partial<Sentinel2FilterState>) => void;
    toggleSentinel2: (
        key: "levels" | "bands",
        value: string
    ) => void;
}

// -----------------------------
// Helpers
// -----------------------------
const roundTo6 = (num: number) => Math.round(num * 1e6) / 1e6;

const formatDateLocal = (d: Date) => d.toLocaleDateString("sv-SE");
const toStartOfDay = (d: string) => `${d}T00:00:00.000Z`;
const toEndOfDay = (d: string) => `${d}T23:59:59.999Z`;

const getDefaultRange = () => {
    const now = new Date();
    const end = formatDateLocal(now);

    const startDate = new Date(now);
    startDate.setDate(startDate.getDate() - 6);

    return {
        start: toStartOfDay(formatDateLocal(startDate)),
        end: toEndOfDay(end),
    };
};

// -----------------------------
// Store
// -----------------------------
export const useFiltersStore = create<FiltersState>((set) => ({
    dataset: Dataset.Sentinel1,
    setDataset: (dataset) => set({ dataset }),

    bbox: { north: 51.08, south: 48.48, east: 19.0, west: 12.07 },
    datetime: getDefaultRange(),

    sentinel1: {
        levels: [],
        sensingTypes: [],
        productTypes: [],
        polarizations: [],
    },

    sentinel2: {
        cloudCover: 100,
        levels: [],
        bands: [],
    },

    setFilters: (newState) => set((state) => ({
        ...state,
        ...newState
    })),

    // -----------------------------
    // BBOX
    // -----------------------------
    setBbox: (bbox) =>
        set((state) => ({
            bbox: { ...state.bbox, ...bbox },
        })),

    setBboxFromMap: (n, s, e, w) =>
        set({
            bbox: {
                north: roundTo6(n),
                south: roundTo6(s),
                east: roundTo6(e),
                west: roundTo6(w),
            },
        }),

    // -----------------------------
    // DATETIME
    // -----------------------------
    setDatetime: (newValues) =>
        set((state) => {
            let start = newValues.start ?? state.datetime.start;
            let end = newValues.end ?? state.datetime.end;

            if (newValues.start && !newValues.start.includes("T")) {
                start = toStartOfDay(newValues.start);
            }

            if (newValues.end && !newValues.end.includes("T")) {
                end = toEndOfDay(newValues.end);
            }

            if (start > end) {
                return {
                    datetime: {
                        start,
                        end: toEndOfDay(start.slice(0, 10)),
                    },
                };
            }

            return { datetime: { start, end } };
        }),

    // -----------------------------
    // Sentinel 1
    // -----------------------------
    toggleSentinel1: (key, value) =>
        set((state) => {
            const arr = state.sentinel1[key];

            return {
                sentinel1: {
                    ...state.sentinel1,
                    [key]: arr.includes(value)
                        ? arr.filter((x) => x !== value)
                        : [...arr, value],
                },
            };
        }),

    // -----------------------------
    // Sentinel 2
    // -----------------------------
    setSentinel2: (partial) =>
        set((state) => ({
            sentinel2: { ...state.sentinel2, ...partial },
        })),

    toggleSentinel2: (key, value) =>
        set((state) => {
            const arr = state.sentinel2[key];

            return {
                sentinel2: {
                    ...state.sentinel2,
                    [key]: arr.includes(value)
                        ? arr.filter((x) => x !== value)
                        : [...arr, value],
                },
            };
        }),
}));