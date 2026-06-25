import {Dataset, DatasetFamily, DatasetToFamily} from "../types/datasets";
import {type ProductFile, type TileLayer, useVisualizationStore} from "../store/useVisualizationStore";
import type {Feature} from "../store/useFeaturesStore";
import {useFiltersStore} from "../store/useFiltersStore";
import {levelsToApi} from "./filterUtils";
import {bandsToApi} from "./visualizationUtils";
import type {ProcessedFileState} from "../types/visualization.ts";

// ======================================================
// APPLY VISUALIZATION RESULTS
// ======================================================

export const applyVisualizationResults = (
    processedFiles: Record<string, ProcessedFileState>,
    outputs: Record<string, { full_product: boolean; wm_tiles?: boolean; }>
) => {
    const newProcessedFiles: ProductFile[] = [];
    const newTileLayers: TileLayer[] = [];

    let availableZoomLevels: number[] = [];

    Object.values(processedFiles).forEach((file) => {
        if (!availableZoomLevels.length) {
            availableZoomLevels = file.wm_tiles_zoom_levels ?? [];
        }

        Object.entries(outputs).forEach(
            ([format, outputConfig]) => {
                const fullProductPath = file.full_product[format as keyof typeof file.full_product];
                const tilePath = file.wm_tiles[format as keyof typeof file.wm_tiles];

                if (outputConfig.full_product && fullProductPath) {
                    newProcessedFiles.push(
                        {
                            path: fullProductPath,
                            name: file.filename,
                            format,
                        }
                    );
                }

                if (outputConfig.wm_tiles && tilePath) {
                    newTileLayers.push(
                        {
                            path: tilePath,
                            name: file.filename,
                            format,
                        }
                    );
                }
            }
        );
    });

    const visualizationStore =
        useVisualizationStore.getState();

    visualizationStore.setProcessedFiles(newProcessedFiles);
    visualizationStore.setTileLayers(newTileLayers);
    visualizationStore.setAvailableZoomLevels(availableZoomLevels);
    visualizationStore.setSelectedTileLayerIndex(newTileLayers.length ? 0 : null);
};

// ======================================================
// VISUALIZATION PAYLOAD
// ======================================================

export const visualizeFeature = (feature: Feature) => {
    const outputs = useVisualizationStore.getState().outputs;

    const payload: any = {
        dataset: feature.dataset,

        properties: {
            quality: 80,
            zoom_levels: [8, 9, 10, 11, 12, 13, 14],
            outputs,
        },
    };

    switch (DatasetToFamily[feature.dataset]) {
        case DatasetFamily.Sentinel:
            payload.metadata = {
                "sentinel:feature_id":
                feature.id,
            };
            break;

        case DatasetFamily.Landsat:
            payload.metadata = {
                "landsat:feature_id":
                feature.id,
            };
            break;

        default:
            throw new Error(
                "Unknown dataset family for dataset: " +
                feature.dataset
            );
    }

    switch (feature.dataset) {
        case Dataset.Sentinel1:
            payload.properties = {
                ...payload.properties,
                ...visualizeSentinel1(feature),
            };
            break;

        case Dataset.Sentinel2:
            payload.properties = {
                ...payload.properties,
                ...visualizeSentinel2(feature),
            };
            break;

        case Dataset.Landsat:
            payload.properties = {
                ...payload.properties,
                ...visualizeLandsat(feature),
            };
            break;

        default:
            throw new Error("Dataset visualization not implemented: " + feature.dataset);
    }

    return payload;
};

// ======================================================
// SENTINEL-1
// ======================================================

const visualizeSentinel1 = (
    feature: Feature
) => {
    const filters = useFiltersStore.getState().sentinel1;

    if (!filters.levels.length) {
        throw new Error("Sentinel-1 filters missing levels");
    }

    if (!filters.productTypes.length) {
        throw new Error("Sentinel-1 filters missing productTypes");
    }

    if (!filters.operationalModes.length) {
        throw new Error("Sentinel-1 filters missing operationalModes");
    }

    if (!filters.polarizations.length) {
        throw new Error("Sentinel-1 filters missing polarizations");
    }

    if (!feature.platform) {
        throw new Error("Feature missing platform");
    }

    return {
        platform: feature.platform,

        filters: {
            levels: levelsToApi(
                feature.dataset,
                filters.levels
            ),
            product_types: filters.productTypes,
            operational_modes: filters.operationalModes,
            polarisation_channels: filters.polarizations,
        },
    };
};

// ======================================================
// SENTINEL-2
// ======================================================

const visualizeSentinel2 = (
    feature: Feature
) => {
    const filters = useFiltersStore.getState().sentinel2;

    const visualization = useVisualizationStore.getState().sentinel2;

    if (filters.cloudCover == null) {
        throw new Error("Sentinel-2 filters missing cloudCover");
    }

    if (!filters.levels.length) {
        throw new Error("Sentinel-2 filters missing levels");
    }

    if (!visualization.bands.length) {
        throw new Error("Sentinel-2 visualization missing bands");
    }

    if (!feature.platform) {
        throw new Error("Feature missing platform");
    }

    return {
        platform: feature.platform,

        filters: {
            cloud_cover:
            filters.cloudCover,

            levels: levelsToApi(
                feature.dataset,
                filters.levels
            ),

            bands: bandsToApi(
                feature.dataset,
                visualization.bands
            ),
        },
    };
};

// ======================================================
// LANDSAT
// ======================================================

const visualizeLandsat = (
    feature: Feature
) => {
    return {"NOTYETIMPLEMENTED": "Not yet implemented!"}; //TODO
};
