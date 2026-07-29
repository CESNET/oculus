import {Dataset} from "../types/datasets";
import {type FiltersStore} from "../store/useFiltersStore";
import type {Sentinel1Filter, Sentinel2Filter} from "../types/filters.ts";

// Defaultní hodnoty pro všechny dataset typy
export const getAllFilterOptions = (dataset: Dataset): Sentinel1Filter | Sentinel2Filter => {
    switch (dataset) {
        case Dataset.Sentinel1:
            return {
                levels: ["0", "1", "2"],
                // productTypes: ["SLC", "GRD"],
                productTypes: ["GRD"], // Only GRD will be filtered since SLC is "partial product" and can't be quite visualized
                operationalModes: ["IW", "EW", "SM", "WV"],
                polarizations: ["HH", "HV", "VV", "VH"],
            } as Sentinel1Filter;

        case Dataset.Sentinel2:
            return {
                //levels: ["0", "1A", "1B", "1C", "2A"],
                /*
                Proč nepoužívat 0, 1A a 1B? Výcuc z ChatGPT:

                U Sentinel-2 se S2MSI0, S2MSI1A a S2MSI1B nepoužívají pro běžné produkty, protože nejde o standardní distribuované produkty MSI Level-1C/Level-2A. Je to trochu matoucí, protože názvy vypadají logicky.
                Historicky Sentinel-2 MSI produktové úrovně vypadají zhruba takto:

                Product type    	Význam	                                                    Použití
                S2MSI0	            Level-0 (raw data)	                                        interní, před zpracováním
                S2MSI1A	            Level-1A	                                                interní předprodukční stupeň
                S2MSI1B	            Level-1B	                                                interní předprodukční stupeň
                S2MSI1C	            Level-1C (Top-of-Atmosphere reflectance)                    běžné distribuované L1C produkty
                S2MSI2A	            Level-2A (Surface Reflectance po atmosférické korekci)	    běžné distribuované L2A produkty
                */
                levels: ["1C", "2A"],
                cloudCover: 100,
            } as Sentinel2Filter;

        case Dataset.Landsat:
            return {
                levels: ["L1", "L2"],
                cloudCover: 100,
            } as Sentinel2Filter; // Landsat zatím používá stejný tvar jako Sentinel2Filters

        default:
            throw new Error("Unknown dataset in getAllOptions");
    }
};

// Efektivní filtry pro fetch
export const getEffectiveFilters = (filters: FiltersStore, dataset: Dataset): FiltersStore => {
    const allOptions = getAllFilterOptions(dataset);

    const effectiveArray = (selected: string[], defaults: string[]) =>
        selected.length ? selected : defaults;

    return {
        ...filters,

        sentinel1: {
            ...filters.sentinel1,
            levels: dataset === Dataset.Sentinel1
                ? effectiveArray(filters.sentinel1.levels, (allOptions as Sentinel1Filter).levels)
                : filters.sentinel1.levels,
            productTypes: dataset === Dataset.Sentinel1
                ? effectiveArray(filters.sentinel1.productTypes, (allOptions as Sentinel1Filter).productTypes)
                : filters.sentinel1.productTypes,
            operationalModes: dataset === Dataset.Sentinel1
                ? effectiveArray(filters.sentinel1.operationalModes, (allOptions as Sentinel1Filter).operationalModes)
                : filters.sentinel1.operationalModes,
            polarizations: dataset === Dataset.Sentinel1
                ? effectiveArray(filters.sentinel1.polarizations, (allOptions as Sentinel1Filter).polarizations)
                : filters.sentinel1.polarizations,
        },

        sentinel2: {
            ...filters.sentinel2,
            levels: dataset === Dataset.Sentinel2
                ? effectiveArray(filters.sentinel2.levels, (allOptions as Sentinel2Filter).levels)
                : filters.sentinel2.levels,
            cloudCover: dataset === Dataset.Sentinel2
                ? filters.sentinel2.cloudCover ?? (allOptions as Sentinel2Filter).cloudCover
                : filters.sentinel2.cloudCover,
        },
    };
};

// Helper pro převod GUI hodnot na API hodnoty
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

// Helpery pro celé pole
export const levelsToApi = (dataset: Dataset, levels: string[]): string[] =>
    levels.map(l => levelToApi(dataset, l));
