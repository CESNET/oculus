import {Dataset} from "../types/datasets";

import type {
    ProcessedFileState,
    ProductFile,
    TileLayer,
    OutputFormat,
} from "../types/visualization";

import {useVisualizationStore} from "../store/useVisualizationStore.ts";


// ======================================================
// PROCESSED FILES
// ======================================================

/**
 * Get generated full product files.
 */
export function getProductFiles(
    processedFiles: Record<string, ProcessedFileState>,
): ProductFile[] {

    return Object.entries(processedFiles)
        .flatMap(([name, file]) =>
            Object.entries(file.outputs)
                .filter(
                    ([, output]) =>
                        output?.full_product !== null &&
                        output?.full_product !== undefined,
                )
                .map(([format, output]) => ({
                    path: output.full_product!,
                    name: `${name}`,
                    format: format as OutputFormat,
                })),
        );
}


/**
 * Get generated WM tile layers.
 */
export function getTileLayers(
    processedFiles: Record<string, ProcessedFileState>,
): TileLayer[] {

    return Object.entries(processedFiles)
        .flatMap(([name, file]) =>
            Object.entries(file.outputs)
                .filter(
                    ([, output]) =>
                        output?.wm_tiles !== null &&
                        output?.wm_tiles !== undefined,
                )
                .map(([format, output]) => ({
                    path: output.wm_tiles!,
                    name,
                    format: format as OutputFormat,
                    zoomLevels: output.wm_tiles_zoom_levels,
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


// ======================================================
// APPLY RESULTS
// ======================================================

export const applyVisualizationResults = (
    processedFiles: Record<string, ProcessedFileState>,
) => {
    const visualizationStore = useVisualizationStore.getState();

    visualizationStore.setProcessedFiles(processedFiles);

    const firstLayer = getTileLayers(processedFiles)[0];

    visualizationStore.setSelectedTileLayerPath(
        firstLayer?.path ?? null,
    );
};