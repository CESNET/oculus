import type {Feature} from "../../types/feature";

import type {
    Sentinel1VisualizationState
} from "../../store/useVisualizationStore.ts";

import type {
    VisualizationProperties,
} from "../../types/visualization/request";

export function buildSentinel1Visualization(
    feature: Feature,
    state: Sentinel1VisualizationState,
): Partial<VisualizationProperties> {
    return {
        visualizations: {},
    };
}
