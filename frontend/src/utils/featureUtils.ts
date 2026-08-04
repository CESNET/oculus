import {Dataset, DatasetFamily, DatasetToFamily} from "../types/datasets";
import {useVisualizationStore} from "../store/useVisualizationStore";
import {useFiltersStore} from "../store/useFiltersStore";
import {levelsToApi} from "./filterUtils";
import {bandsToApi} from "./visualizationUtils";
import type {ProcessedFileState} from "../types/visualization.ts";
import type {Feature} from "../types/feature.ts";

// ======================================================
// APPLY VISUALIZATION RESULTS
// ======================================================

export const applyVisualizationResults = (
    processedFiles: Record<string, ProcessedFileState>
) => {
    const visualizationStore = useVisualizationStore.getState();

    visualizationStore.setProcessedFiles(processedFiles);

    const firstLayer =
        Object.values(processedFiles)
            .find(file =>
                Object.values(file.wm_tiles)
                    .some(path => path !== null)
            );

    if (firstLayer) {
        const firstPath = Object.values(firstLayer.wm_tiles).find(path => path !== null);
        visualizationStore.setSelectedTileLayerPath(firstPath ?? null);
    }
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

    if (!visualization.selectedBands.length) {
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
                visualization.selectedBands
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
    return {"NOTYETIMPLEMENTED": "Not yet implemented!", "FEATURE": feature}; //TODO
};
