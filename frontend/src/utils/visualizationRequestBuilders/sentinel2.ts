import type {Feature} from "../../types/feature.ts";

import type {
    Sentinel2VisualizationState
} from "../../store/useVisualizationStore.ts";

import {
    bandsToApi
} from "../visualizationUtils.ts";

import type {
    VisualizationProperties
} from "../../types/visualization/request.ts";


export function buildSentinel2Visualization(
    feature: Feature,
    visualization: Sentinel2VisualizationState,
): Partial<VisualizationProperties> {
    const visualizations: Record<string, unknown> = {};

    if (visualization.selectedBands.length) {
        visualizations.bands = bandsToApi(
            feature.dataset,
            visualization.selectedBands,
        );
    }


    if (visualization.generateRGB) {
        visualizations.rgb_composite = {
            red: `B${visualization.selectedRGBComposite.red.padStart(2, "0")}`,
            green: `B${visualization.selectedRGBComposite.green.padStart(2, "0")}`,
            blue: `B${visualization.selectedRGBComposite.blue.padStart(2, "0")}`,
        };
    }


    if (visualization.selectedPresetIds.length) {
        visualizations.presets = visualization.selectedPresetIds;
    }


    return {visualizations,};
}
