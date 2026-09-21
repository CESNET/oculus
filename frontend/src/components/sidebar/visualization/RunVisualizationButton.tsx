import {useFeaturesStore} from "../../../store/useFeaturesStore";
import {useVisualizationStore} from "../../../store/useVisualizationStore";

import {runVisualization} from "../../../service/visualization/visualizationService.ts";

interface RunVisualizationButtonProps {
    featureId?: string;
}

export default function RunVisualizationButton({
                                                   featureId: propFeatureId,
                                               }: RunVisualizationButtonProps) {
    const storeFeatureId = useVisualizationStore(
        (s) => s.featureId
    );

    const featureId = propFeatureId ?? storeFeatureId;

    const feature = useFeaturesStore(
        (s) => featureId ? s.featuresById[featureId] : undefined
    );

    return (
        <button
            className="btn btn-primary w-100 mt-3"
            disabled={!feature}
            onClick={() => {
                if (feature) {
                    runVisualization(feature);
                }
            }}
        >
            Render Visualization
        </button>
    );
}