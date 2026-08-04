import {
    SENTINEL2_VISUALIZATION_MODE,
} from "../../../types/visualization/sentinel2";

import {useVisualizationStore} from "../../../store/useVisualizationStore";

import Sentinel2VisualizationModeSelector from "./Sentinel2VisualizationModeSelector.tsx";
import Sentinel2SingleBandOptions from "./Sentinel2SingleBandOptions.tsx";
import Sentinel2RGBCompositeOptions from "./Sentinel2RGBCompositeOptions.tsx";
import Sentinel2PresetOptions from "./Sentinel2PresetOptions";

export default function Sentinel2VisualizationOptions() {
    const sentinel2 = useVisualizationStore(s => s.sentinel2);

    return (
        <>
            <Sentinel2VisualizationModeSelector />

            {sentinel2.mode === SENTINEL2_VISUALIZATION_MODE.SINGLE_BANDS && (
                <Sentinel2SingleBandOptions />
            )}

            {sentinel2.mode === SENTINEL2_VISUALIZATION_MODE.CUSTOM_RGB && (
                <Sentinel2RGBCompositeOptions />
            )}

            {sentinel2.mode === SENTINEL2_VISUALIZATION_MODE.PRESETS && (
                <Sentinel2PresetOptions />
            )}
        </>
    );
}