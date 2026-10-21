import ButtonGroup from "../ButtonGroup";

import { useVisualizationStore } from "../../../store/useVisualizationStore";

import {
    SENTINEL2_PRESET_OPTIONS,
    type Sentinel2PresetId,
} from "../../../types/visualization/sentinel2";


export default function Sentinel2PresetOptions() {
    const selectedPresets = useVisualizationStore(
        (s) => s.sentinel2.selectedPresetIds
    );

    const toggleSentinel2Preset = useVisualizationStore(
        (s) => s.toggleSentinel2Preset
    );

    return (
        <ButtonGroup<Sentinel2PresetId>
            multiple
            label="Presets"
            values={SENTINEL2_PRESET_OPTIONS}
            selected={selectedPresets}
            onToggle={toggleSentinel2Preset}
        />
    );
}