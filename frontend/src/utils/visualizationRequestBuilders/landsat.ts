import type {Feature} from "../../types/feature";

import type {
    LandsatVisualizationState
} from "../../store/useVisualizationStore.ts";

import type {
    VisualizationProperties,
} from "../../types/visualization/request";

export function buildLandsatVisualization(
    feature: Feature,
    state: LandsatVisualizationState
): Partial<VisualizationProperties> {
    return {
        visualizations: {},
    };
}