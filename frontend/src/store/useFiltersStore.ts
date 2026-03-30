import { create } from "zustand";

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
    cloudCover: number;
    levels: string[];
    bands: string[];
}

export interface FiltersState {
    bbox: BoundingBox;
    datetime: Datetime;
    sentinel1: Sentinel1FilterState;
    sentinel2: Sentinel2FilterState;

    setBbox: (bbox: Partial<BoundingBox>) => void;
    setBboxFromMap: (north: number, south: number, east: number, west: number) => void;
    setDatetime: (datetime: Partial<{ start: string; end: string }>) => void;
}

// -----------------------------
// Pomocné funkce
// -----------------------------
const roundTo6 = (num: number) => Math.round(num * 1000000) / 1000000;

// 👉 BEZ UTC bugu
const formatDateLocal = (d: Date) =>
    d.toLocaleDateString("sv-SE"); // YYYY-MM-DD

const toStartOfDay = (date: string) =>
    `${date}T00:00:00.000Z`;

const toEndOfDay = (date: string) =>
    `${date}T23:59:59.999Z`;

// 👉 DEFAULT: posledních 7 dní
const getDefaultRange = () => {
    const now = new Date();

    const end = formatDateLocal(now);

    const startDate = new Date(now);
    startDate.setDate(startDate.getDate() - 6);

    const start = formatDateLocal(startDate);

    return {
        start: toStartOfDay(start),
        end: toEndOfDay(end),
    };
};

// -----------------------------
// Store
// -----------------------------
export const useFiltersStore = create<FiltersState>((set) => ({
    bbox: { north: 51.08, south: 48.48, east: 19.00, west: 12.07 },

    datetime: getDefaultRange(),

    sentinel1: { levels: [], sensingTypes: [], productTypes: [], polarizations: [] },
    sentinel2: { cloudCover: 100, levels: [], bands: [] },

    // -----------------------------
    // BBOX
    // -----------------------------
    setBbox: (bbox) => set((state) => ({
        bbox: { ...state.bbox, ...bbox }
    })),

    setBboxFromMap: (north, south, east, west) => set({
        bbox: {
            north: roundTo6(north),
            south: roundTo6(south),
            east: roundTo6(east),
            west: roundTo6(west)
        }
    }),

    // -----------------------------
    // DATETIME
    // -----------------------------
    setDatetime: (newValues) => set((state) => {
        let start = newValues.start ?? state.datetime.start;
        let end = newValues.end ?? state.datetime.end;

        // 👉 normalizace (když přijde jen YYYY-MM-DD)
        if (newValues.start && !newValues.start.includes("T")) {
            start = toStartOfDay(newValues.start);
        }

        if (newValues.end && !newValues.end.includes("T")) {
            end = toEndOfDay(newValues.end);
        }

        // 👉 ochrana: start <= end
        if (start > end) {
            return {
                datetime: {
                    start,
                    end: toEndOfDay(start.slice(0, 10)),
                }
            };
        }

        return {
            datetime: { start, end }
        };
    }),
}));