import {
    Dataset,
    DatasetFamily,
    DatasetToFamily,
} from "../types/datasets";

import {
    useVisualizationStore,
    type VisualizationState,
} from "../store/useVisualizationStore";

import type {Feature} from "../types/feature";

import type {
    VisualizationRequest,
    VisualizationProperties,
} from "../types/visualization/request";

import {
    buildSentinel1Visualization,
} from "./visualizationRequestBuilders/sentinel1";

import {
    buildSentinel2Visualization,
} from "./visualizationRequestBuilders/sentinel2";

import {
    buildLandsatVisualization,
} from "./visualizationRequestBuilders/landsat";


// ======================================================
// DATASET BUILDERS
// ======================================================

const buildDatasetVisualization = (
    feature: Feature,
    state: VisualizationState,
): Partial<VisualizationProperties> => {
    switch (feature.dataset) {
        case Dataset.Sentinel1:
            return buildSentinel1Visualization(
                feature,
                state.sentinel1,
            );

        case Dataset.Sentinel2:
            return buildSentinel2Visualization(
                feature,
                state.sentinel2,
            );

        case Dataset.Landsat:
            return buildLandsatVisualization(
                feature,
                state.landsat,
            );

        default:
            throw new Error(`Visualization not supported for dataset: ${feature.dataset}`);
    }
};

// ======================================================
// REQUEST BUILDER
// ======================================================

export const getVisualizationRequestPayload = (feature: Feature,): VisualizationRequest => {
    const state = useVisualizationStore.getState();

    const datasetVisualization = buildDatasetVisualization(feature, state);

    return {
        dataset: feature.dataset,

        properties: {
            quality: 80,
            zoom_levels: [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
            ],
            outputs: state.outputs,
            ...datasetVisualization,
        },

        metadata: buildMetadata(feature),
    };
};


// ======================================================
// METADATA
// ======================================================

const buildMetadata = (feature: Feature): Record<string, string> => {
    switch (DatasetToFamily[feature.dataset]) {
        case DatasetFamily.Sentinel:
            return {
                "sentinel:feature_id": feature.id,
            };

        case DatasetFamily.Landsat:
            return {
                "landsat:feature_id": feature.id,
            };

        default:
            throw new Error(`Unknown dataset family: ${feature.dataset}`,);
    }
};
