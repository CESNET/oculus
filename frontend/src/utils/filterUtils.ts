import {Dataset} from "../types/datasets";

import type {FiltersStore} from "../store/useFiltersStore";

import type {
    Sentinel1Filter,
    Sentinel2Filter,
} from "../types/filters";


// ======================================================
// DEFAULT FILTER OPTIONS
// ======================================================

export const getAllFilterOptions = (dataset: Dataset): Sentinel1Filter | Sentinel2Filter => {

    switch (dataset) {
        case Dataset.Sentinel1:

            return {
                levels: [
                    "0",
                    "1",
                    "2",
                ],

                productTypes: [
                    "GRD",
                ],

                operationalModes: [
                    "IW",
                    "EW",
                    "SM",
                    "WV",
                ],

                polarizations: [
                    "HH",
                    "HV",
                    "VV",
                    "VH",
                ],
            } as Sentinel1Filter;


        case Dataset.Sentinel2:

            return {
                levels: [
                    "1C",
                    "2A",
                ],

                cloudCover: 100,
            } as Sentinel2Filter;


        case Dataset.Landsat:

            return {
                levels: [
                    "L1",
                    "L2",
                ],

                cloudCover: 100,
            } as Sentinel2Filter; // Landsat zatím používá stejný tvar jako Sentinel2Filters


        default:
            throw new Error(
                `Unknown dataset: ${dataset}`,
            );
    }
};


// ======================================================
// EFFECTIVE FILTERS
// ======================================================

export const getEffectiveFilters = (
    filters: FiltersStore,
    dataset: Dataset,
): FiltersStore => {

    const allOptions =
        getAllFilterOptions(dataset);


    const effectiveArray = (
        selected: string[],
        defaults: string[],
    ) =>
        selected.length
            ? selected
            : defaults;


    return {

        ...filters,


        sentinel1: {

            ...filters.sentinel1,


            levels:
                dataset === Dataset.Sentinel1
                    ? effectiveArray(
                        filters.sentinel1.levels,
                        (allOptions as Sentinel1Filter).levels,
                    )
                    : filters.sentinel1.levels,


            productTypes:
                dataset === Dataset.Sentinel1
                    ? effectiveArray(
                        filters.sentinel1.productTypes,
                        (allOptions as Sentinel1Filter).productTypes,
                    )
                    : filters.sentinel1.productTypes,


            operationalModes:
                dataset === Dataset.Sentinel1
                    ? effectiveArray(
                        filters.sentinel1.operationalModes,
                        (allOptions as Sentinel1Filter).operationalModes,
                    )
                    : filters.sentinel1.operationalModes,


            polarizations:
                dataset === Dataset.Sentinel1
                    ? effectiveArray(
                        filters.sentinel1.polarizations,
                        (allOptions as Sentinel1Filter).polarizations,
                    )
                    : filters.sentinel1.polarizations,
        },


        sentinel2: {

            ...filters.sentinel2,


            levels:
                dataset === Dataset.Sentinel2
                    ? effectiveArray(
                        filters.sentinel2.levels,
                        (allOptions as Sentinel2Filter).levels,
                    )
                    : filters.sentinel2.levels,


            cloudCover:
                dataset === Dataset.Sentinel2
                    ? filters.sentinel2.cloudCover ??
                    (allOptions as Sentinel2Filter).cloudCover
                    : filters.sentinel2.cloudCover,
        },
    };
};


// ======================================================
// API CONVERSION
// ======================================================

export const levelToApi = (
    dataset: Dataset,
    level: string,
): string => {

    switch (dataset) {

        case Dataset.Sentinel1:
            return `LEVEL${level}`;


        case Dataset.Sentinel2:
            return `S2MSI${level}`;


        case Dataset.Landsat:

            return level.startsWith("L")
                ? level
                : `L${level}`;


        default:
            return level;
    }
};


export const levelsToApi = (
    dataset: Dataset,
    levels: string[],
): string[] =>
    levels.map(
        level => levelToApi(dataset, level),
    );
