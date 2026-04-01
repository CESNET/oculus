import {type FiltersState} from "../store/useFiltersStore";
import {Dataset} from "../types/datasets";
import {fetchCDSEFeatures} from "./fetchCDSEFeatures.ts";

export const fetchFeatures = async (
    filters: FiltersState,
    dataset: Dataset
) => {
    switch (dataset) {
        case Dataset.Sentinel1:
        case Dataset.Sentinel2:
            return fetchCDSEFeatures(filters, dataset);

        case Dataset.Landsat:
            // TODO: implement later
            console.warn("Landsat fetch not implemented yet");
            return [];

        default:
            throw new Error("Unknown dataset: " + dataset);
    }
};