import type {Feature} from "../../types/feature.ts";

import type {
    Sentinel1VisualizationState,
} from "../../store/useVisualizationStore.ts";

import type {
    VisualizationProperties,
} from "../../types/visualization/request.ts";


export function buildSentinel1VisualizationRequest(
    _feature: Feature,
    visualization: Sentinel1VisualizationState,
): Partial<VisualizationProperties> {

    const visualizations: Record<string, unknown> = {};

    if (visualization.selectedPolarizations.length) {
        visualizations.polarizations = visualization.selectedPolarizations;
    }

    return {
        visualizations,
    };
}