import ButtonGroup from "../ButtonGroup.tsx";

import {useVisualizationStore} from "../../../store/useVisualizationStore.ts";

import {SENTINEL2_BAND_OPTIONS} from "../../../types/visualization/sentinel2.ts";


export default function Sentinel2SingleBandOptions() {
    const selectedBands = useVisualizationStore(
        s => s.sentinel2.selectedBands
    );

    const toggleSentinel2Band = useVisualizationStore(
        s => s.toggleSentinel2Band
    );

    return (
        <ButtonGroup
            multiple
            label="Bands"
            values={SENTINEL2_BAND_OPTIONS}
            selected={selectedBands}
            onToggle={toggleSentinel2Band}
        />
    );
}
