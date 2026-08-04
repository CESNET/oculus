import {useVisualizationStore} from "../../../store/useVisualizationStore.ts";

import Sentinel2BandSelector from "./Sentinel2BandSelector.tsx";

import type {
    Sentinel2RGBComposite,
    Sentinel2SpectralBand,
} from "../../../types/visualization/sentinel2.ts";


export default function Sentinel2RGBCompositeOptions() {
    const rgb = useVisualizationStore(
        s => s.sentinel2.selectedRGBComposite
    );

    const setSentinel2 = useVisualizationStore(
        s => s.setSentinel2
    );

    const updateChannel = (
        channel: keyof Sentinel2RGBComposite,
        value: Sentinel2SpectralBand,
    ) => {
        setSentinel2({
            selectedRGBComposite: {
                ...rgb,
                [channel]: value,
            },
        });
    };

    return (
        <>
            <Sentinel2BandSelector
                label="Red"
                value={rgb.red}
                onChange={(value) =>
                    updateChannel("red", value)
                }
            />

            <Sentinel2BandSelector
                label="Green"
                value={rgb.green}
                onChange={(value) =>
                    updateChannel("green", value)
                }
            />

            <Sentinel2BandSelector
                label="Blue"
                value={rgb.blue}
                onChange={(value) =>
                    updateChannel("blue", value)
                }
            />
        </>
    );
}
