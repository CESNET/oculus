import { useFeaturesStore } from "../../../store/useFeaturesStore";
import { useVisualizationStore } from "../../../store/useVisualizationStore";

import { runVisualization } from "../../../service/visualizationService";


export default function RunVisualizationButton() {
    const featureId = useVisualizationStore(
        (s) => s.featureId
    );

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
            Re-render Visualization
        </button>
    );
}