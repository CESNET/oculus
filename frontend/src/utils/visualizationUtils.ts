import {Dataset} from "../types/datasets";
import {type Sentinel1VisualizationState, type Sentinel2VisualizationState} from "../store/useVisualizationStore";

// Defaultní hodnoty pro všechny dataset typy
export const getAllVisualizationOptions = (dataset: Dataset): Sentinel1VisualizationState | Sentinel2VisualizationState => {
    switch (dataset) {
        case Dataset.Sentinel1:
            return {} as Sentinel1VisualizationState;

        case Dataset.Sentinel2:
            return {
                bands: ["1", "2", "3", "4", "5", "6", "7", "8", "8A", "9", "10", "11", "12", "TCI"],
            } as Sentinel2VisualizationState;

        case Dataset.Landsat:
            return {
                bands: ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            } as Sentinel2VisualizationState; // Landsat zatím používá stejný tvar jako Sentinel2

        default:
            throw new Error("Unknown dataset in getAllOptions");
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

export const bandsToApi = (dataset: Dataset, bands: string[]): string[] =>
    bands.map(b => bandToApi(dataset, b));
