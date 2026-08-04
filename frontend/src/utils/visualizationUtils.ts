import {Dataset} from "../types/datasets";

import type {
    ProcessedFileState,
    ProductFile,
    TileLayer
} from "../types/visualization";

export function getProductFiles(
    processedFiles: Record<string, ProcessedFileState>
): ProductFile[] {

    return Object.values(processedFiles)
        .flatMap(file =>
            Object.entries(file.full_product)
                .filter(
                    ([, path]) => path !== null
                )
                .map(([format, path]) => ({
                    path: path!,
                    name: file.filename,
                    format,
                }))
        );
}

export function getTileLayers(
    processedFiles: Record<string, ProcessedFileState>
): TileLayer[] {
    return Object.values(processedFiles)
        .flatMap(file =>
            Object.entries(file.wm_tiles)
                .filter(
                    ([, path]) => path !== null
                )
                .map(([format, path]) => ({
                    path: path!,
                    name: file.filename,
                    format,
                    zoomLevels:
                    file.wm_tiles_zoom_levels,
                }))
        );
}

export function getSelectedTileLayer(
    processedFiles: Record<string, ProcessedFileState>,
    selectedPath: string | null
): TileLayer | null {
    if (!selectedPath) {
        return null;
    }

    return getTileLayers(processedFiles).find(
        layer =>
            layer.path === selectedPath
    ) ?? null;
}

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
