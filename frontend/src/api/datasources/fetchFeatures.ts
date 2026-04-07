import { type FiltersState } from "../../store/useFiltersStore.ts";
import { Dataset } from "../../types/datasets.ts";
import { fetchCDSEFeatures } from "./fetchCDSEFeatures.ts";

export const fetchFeatures = async (
    filters: FiltersState,
    dataset: Dataset,
    signal?: AbortSignal
) => {
    switch (dataset) {
        case Dataset.Sentinel1:
        case Dataset.Sentinel2:
            return fetchCDSEFeatures(filters, dataset, signal);

        case Dataset.Landsat:
            console.warn("Landsat fetch not implemented yet");
            return [];

        default:
            throw new Error("Unknown dataset: " + dataset);
    }
};