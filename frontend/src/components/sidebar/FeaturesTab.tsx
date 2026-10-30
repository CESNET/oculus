import {useFeaturesStore} from "../../store/useFeaturesStore";
import FeatureCard from "./features/FeatureCard";
import type {Feature} from "../../types/feature.ts";

export default function FeaturesTab() {
    const featureIds = useFeaturesStore((s) => s.featureIds);
    const featuresById = useFeaturesStore((s) => s.featuresById);

    const features = featureIds
        .map((id) => featuresById[id])
        .filter(Boolean);

    if (!features.length) {
        return (
            <div className="text-center py-5">
                No features loaded
            </div>
        );
    }

    // TODO: Add global visualization options (formats, JPEG quality, etc.)

    return (
        <div className="features-list">
            {features.map((feature: Feature) => (
                <FeatureCard
                    key={feature.id}
                    feature={feature}
                />
            ))}
        </div>
    );
}
