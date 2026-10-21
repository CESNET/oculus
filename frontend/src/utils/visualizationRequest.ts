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
    buildSentinel1VisualizationRequest,
} from "./visualizationRequestBuilders/sentinel1";

import {
    buildSentinel2VisualizationRequest,
} from "./visualizationRequestBuilders/sentinel2";

import {
    buildLandsatVisualizationRequest,
} from "./visualizationRequestBuilders/landsat";


// ======================================================
// DATASET BUILDERS
// ======================================================

const buildDatasetVisualizationRequest = (
    feature: Feature,
    state: VisualizationState,
): Partial<VisualizationProperties> => {
    switch (feature.dataset) {
        case Dataset.Sentinel1:
            return buildSentinel1VisualizationRequest(
                feature,
                state.sentinel1,
            );

        case Dataset.Sentinel2:
            return buildSentinel2VisualizationRequest(
                feature,
                state.sentinel2,
            );

        case Dataset.Landsat:
            return buildLandsatVisualizationRequest(
                feature,
                state.landsat,
            );

        default:
            throw new Error(`Visualization request not supported for dataset: ${feature.dataset}`);
    }
};


// ======================================================
// REQUEST BUILDER
// ======================================================

export const getVisualizationRequestPayload = (feature: Feature,): VisualizationRequest => {
    const state = useVisualizationStore.getState();

    const datasetVisualizationRequest = buildDatasetVisualizationRequest(feature, state);

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

            ...datasetVisualizationRequest,
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