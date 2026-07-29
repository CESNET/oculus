import type { FiltersStore } from "../../store/useFiltersStore";
import { Dataset } from "../../types/datasets";

import { fetchSentinel1Features } from "./fetchSentinel1Features";
import { fetchSentinel2Features } from "./fetchSentinel2Features";

export async function fetchFeatures(
    filters: FiltersStore,
    dataset: Dataset,
    signal?: AbortSignal,
) {
    switch (dataset) {
        case Dataset.Sentinel1:
            return fetchSentinel1Features(filters, signal);

        case Dataset.Sentinel2:
            return fetchSentinel2Features(filters, signal);

        case Dataset.Landsat:
            console.warn("Landsat fetch not implemented yet");
            return [];

        default:
            throw new Error(`Unsupported dataset: ${dataset}`);
    }
}