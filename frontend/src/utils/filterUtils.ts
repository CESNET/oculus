import {Dataset} from "../types/datasets";
import {type FiltersState} from "../store/useFiltersStore";
import {type Sentinel1FilterState, type Sentinel2FilterState} from "../store/useFiltersStore";

// 1️⃣ Defaultní hodnoty pro všechny dataset typy
export const getAllOptions = (dataset: Dataset): Sentinel1FilterState | Sentinel2FilterState => {
    switch (dataset) {
        case Dataset.Sentinel1:
            return {
                levels: ["0", "1", "2"],
                // productTypes: ["SLC", "GRD"],
                productTypes: ["GRD"], // Only GRD will be filtered since SLC is "partial product" and can't be quite visualized
                operationalModes: ["IW", "EW", "SM", "WV"],
                polarizations: ["HH", "HV", "VV", "VH"],
            } as Sentinel1FilterState;

        case Dataset.Sentinel2:
            return {
                levels: ["0", "1A", "1B", "1C", "2A"],
                bands: ["1", "2", "3", "4", "5", "6", "7", "8", "8A", "9", "10", "11", "12", "TCI"],
                cloudCover: 100,
            } as Sentinel2FilterState;

        case Dataset.Landsat:
            return {
                levels: ["L1", "L2"],
                bands: ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
                cloudCover: 100,
            } as Sentinel2FilterState; // Landsat zatím používá stejný tvar jako Sentinel2Filters

        default:
            throw new Error("Unknown dataset in getAllOptions");
    }
};

// 2️⃣ Efektivní filtry pro fetch
export const getEffectiveFilters = (filters: FiltersState, dataset: Dataset): FiltersState => {
    const allOptions = getAllOptions(dataset);

    const effectiveArray = (selected: string[], defaults: string[]) =>
        selected.length ? selected : defaults;

    return {
        ...filters,
        sentinel1: {
            ...filters.sentinel1,
            levels: dataset === Dataset.Sentinel1
                ? effectiveArray(filters.sentinel1.levels, (allOptions as Sentinel1FilterState).levels)
                : filters.sentinel1.levels,
            productTypes: dataset === Dataset.Sentinel1
                ? effectiveArray(filters.sentinel1.productTypes, (allOptions as Sentinel1FilterState).productTypes)
                : filters.sentinel1.productTypes,
            operationalModes: dataset === Dataset.Sentinel1
                ? effectiveArray(filters.sentinel1.operationalModes, (allOptions as Sentinel1FilterState).operationalModes)
                : filters.sentinel1.operationalModes,
            polarizations: dataset === Dataset.Sentinel1
                ? effectiveArray(filters.sentinel1.polarizations, (allOptions as Sentinel1FilterState).polarizations)
                : filters.sentinel1.polarizations,
        },
        sentinel2: {
            ...filters.sentinel2,
            levels: dataset === Dataset.Sentinel2
                ? effectiveArray(filters.sentinel2.levels, (allOptions as Sentinel2FilterState).levels)
                : filters.sentinel2.levels,
            bands: dataset === Dataset.Sentinel2
                ? effectiveArray(filters.sentinel2.bands, (allOptions as Sentinel2FilterState).bands)
                : filters.sentinel2.bands,
            cloudCover: dataset === Dataset.Sentinel2
                ? filters.sentinel2.cloudCover ?? (allOptions as Sentinel2FilterState).cloudCover
                : filters.sentinel2.cloudCover,
        },
    };
};

// 3️⃣ Helper pro převod GUI hodnot na API hodnoty
export const levelToApi = (dataset: Dataset, level: string): string => {
    switch (dataset) {
        case Dataset.Sentinel1:
            return `LEVEL${level}`;
        case Dataset.Sentinel2:
            return `S2MSI${level}`;
        case Dataset.Landsat:
            return level.startsWith("L") ? level : `L${level}`;
        default:
            return level;
    }
};

export const bandToApi = (dataset: Dataset, band: string): string => {
    if (dataset === Dataset.Sentinel2) {
        return band === "TCI" ? "TCI" : `B${band.padStart(2, "0")}`;
    } else if (dataset === Dataset.Landsat) {
        return `B${band.padStart(2, "0")}`;
    }
    return band; // Sentinel1 bands zatím nejsou relevantní
};

// 4️⃣ Helpery pro celé pole
export const levelsToApi = (dataset: Dataset, levels: string[]): string[] =>
    levels.map(l => levelToApi(dataset, l));

export const bandsToApi = (dataset: Dataset, bands: string[]): string[] =>
    bands.map(b => bandToApi(dataset, b));