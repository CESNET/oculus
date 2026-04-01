import {Dataset} from "../types/datasets";
import {type FiltersState} from "../store/useFiltersStore";
import {type Sentinel1FilterState, type Sentinel2FilterState} from "../store/useFiltersStore";

// 1️⃣ Defaultní hodnoty pro všechny dataset typy
export const getAllOptions = (dataset: Dataset): Sentinel1FilterState | Sentinel2FilterState => {
    switch (dataset) {
        case Dataset.Sentinel1:
            return {
                levels: ["0", "1", "2"],
                productTypes: ["SLC", "GRD"],
                sensingTypes: ["IW", "EW", "SM", "WV"],
                polarizations: ["HH", "HV", "VV", "VH"],
            } as Sentinel1FilterState;

        case Dataset.Sentinel2:
            return {
                levels: ["0", "1A", "1B", "1C", "2A"],
                bands: ["1", "2", "3", "4", "5", "6", "7", "8", "8A", "9", "10", "11", "12", "TCI"],
                cloudCover: 100,
            } as Sentinel2FilterState;

        case Dataset.Landsat:
            // ⭐ placeholder pro budoucí implementaci
            return {
                levels: ["L1", "L2"],           // například levely L1 a L2
                bands: ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9"],
                cloudCover: 100,                // defaultně max 100%
            } as Sentinel2FilterState;  // Landsat zatím používá stejný tvar jako Sentinel2Filters

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
            sensingTypes: dataset === Dataset.Sentinel1
                ? effectiveArray(filters.sentinel1.sensingTypes, (allOptions as Sentinel1FilterState).sensingTypes)
                : filters.sentinel1.sensingTypes,
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