import {useVisualizationStore} from "../../../store/useVisualizationStore.ts";
import {SENTINEL2_VISUALIZATION_MODE} from "../../../types/visualization/sentinel2.ts";
import ButtonGroup from "../ButtonGroup.tsx";

export default function Sentinel2VisualizationModeSelector() {
    const mode = useVisualizationStore(
        s => s.sentinel2.mode
    );

    const setSentinel2 = useVisualizationStore(
        s => s.setSentinel2
    );

    return (
        <ButtonGroup
            label="Visualization"

            values={[
                {
                    label: "Single Bands",
                    value: SENTINEL2_VISUALIZATION_MODE.SINGLE_BANDS,
                },
                {
                    label: "RGB Composite",
                    value: SENTINEL2_VISUALIZATION_MODE.CUSTOM_RGB,
                },
                {
                    label: "Presets",
                    value: SENTINEL2_VISUALIZATION_MODE.PRESETS,
                },
            ]}

            selected={mode}

            onChange={(mode) => {
                if (
                    mode === SENTINEL2_VISUALIZATION_MODE.CUSTOM_RGB &&
                    !useVisualizationStore.getState().sentinel2.generateRGB
                ) {
                    setSentinel2({
                        mode,
                        generateRGB: true,
                    });
                    return;
                }

                setSentinel2({mode});
            }}
        />
    );
}
