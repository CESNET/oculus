import {Dataset} from "../types/datasets";

import type {
    ProcessedFileState,
    ProductFile,
    TileLayer,
} from "../types/visualization";


// ======================================================
// PROCESSED FILES
// ======================================================

/**
 * Get generated full product files.
 */
export function getProductFiles(
    processedFiles: Record<string, ProcessedFileState>,
): ProductFile[] {

    return Object.values(processedFiles)
        .flatMap(file =>
            Object.entries(file.full_product)
                .filter(
                    ([, path]) =>
                        path !== null,
                )
                .map(([format, path]) => ({
                    path: path!,
                    name: file.filename,
                    format,
                })),
        );
}


/**
 * Get generated WM tile layers.
 */
export function getTileLayers(
    processedFiles: Record<string, ProcessedFileState>,
): TileLayer[] {

    return Object.values(processedFiles)
        .flatMap(file =>
            Object.entries(file.wm_tiles)
                .filter(
                    ([, path]) =>
                        path !== null,
                )
                .map(([format, path]) => ({
                    path: path!,
                    name: file.filename,
                    format,
                    zoomLevels:
                    file.wm_tiles_zoom_levels,
                })),
        );
}


/**
 * Find selected tile layer by path.
 */
export function getSelectedTileLayer(
    processedFiles: Record<string, ProcessedFileState>,
    selectedPath: string | null,
): TileLayer | null {

    if (!selectedPath) {
        return null;
    }

    return (
        getTileLayers(processedFiles)
            .find(
                layer =>
                    layer.path === selectedPath,
            )
        ?? null
    );
}


// ======================================================
// BAND CONVERSION
// ======================================================

/**
 * Convert frontend band name to backend API band name.
 *
 * Examples:
 * Sentinel-2:
 *   "4"   -> "B04"
 *   "8"   -> "B08"
 *   "TCI" -> "TCI"
 *
 * Landsat:
 *   "4"   -> "B04"
 */
export const bandToApi = (
    dataset: Dataset,
    band: string,
): string => {

    switch (dataset) {

        case Dataset.Sentinel2:
            return band === "TCI"
                ? "TCI"
                : `B${band.padStart(2, "0")}`;

        case Dataset.Landsat:
            return `B${band.padStart(2, "0")}`;

        case Dataset.Sentinel1:

        // eslint-disable-next-line no-fallthrough
        default:
            return band;
    }
};


/**
 * Convert multiple bands to API representation.
 */
export const bandsToApi = (
    dataset: Dataset,
    bands: string[],
): string[] =>
    bands.map(
        band =>
            bandToApi(
                dataset,
                band,
            ),
    );
