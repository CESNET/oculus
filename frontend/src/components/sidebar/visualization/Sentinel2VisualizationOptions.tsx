import {
    useVisualizationStore,
} from "../../../store/useVisualizationStore";

import {
    SENTINEL2_VISUALIZATION_MODE,
} from "../../../types/visualization/sentinel2";

import Sentinel2VisualizationModeSelector from "./Sentinel2VisualizationModeSelector";
import Sentinel2SingleBandOptions from "./Sentinel2SingleBandOptions";
import Sentinel2RGBCompositeOptions from "./Sentinel2RGBCompositeOptions";
import Sentinel2PresetOptions from "./Sentinel2PresetOptions";
import RunVisualizationButton from "./RunVisualizationButton";


export default function Sentinel2Options() {
    const mode = useVisualizationStore(
        (s) => s.sentinel2.mode
    );

    return (
        <>
            <Sentinel2VisualizationModeSelector />

            {mode === SENTINEL2_VISUALIZATION_MODE.SINGLE_BANDS && (
                <Sentinel2SingleBandOptions />
            )}

            {mode === SENTINEL2_VISUALIZATION_MODE.CUSTOM_RGB && (
                <Sentinel2RGBCompositeOptions />
            )}

            {mode === SENTINEL2_VISUALIZATION_MODE.PRESETS && (
                <Sentinel2PresetOptions />
            )}

            <RunVisualizationButton />
        </>
    );
}