import type {Feature} from "../../types/feature";

import type {
    LandsatVisualizationState
} from "../../store/useVisualizationStore.ts";

import type {
    VisualizationProperties,
} from "../../types/visualization/request";

export function buildLandsatVisualization(
    //todo odebrat _
    _feature: Feature,
    _state: LandsatVisualizationState
): Partial<VisualizationProperties> {
    return {
        visualizations: {},
    };
}