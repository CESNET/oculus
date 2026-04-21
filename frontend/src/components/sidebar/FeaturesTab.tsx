import {type Feature, useFeaturesStore} from "../../store/useFeaturesStore";
import FeatureCard from "./features/FeatureCard";

export default function FeaturesTab() {
    const featureIds = useFeaturesStore((s) => s.featureIds);
    const featuresById = useFeaturesStore((s) => s.featuresById);

    const features = featureIds
        .map((id) => featuresById[id])
        .filter(Boolean);

    if (!features.length) {
        return <div className="text-center py-5">No features loaded</div>;
    }

    // TODO na horní okraj by to chtělo přidat možnosti pro vizualizaci - tedy formáty, JPEG quality...

    return (
        <div className="features-list">
            {features.map((f: Feature) => (
                <FeatureCard key={f.id} feature={f} />
            ))}
        </div>
    );
}