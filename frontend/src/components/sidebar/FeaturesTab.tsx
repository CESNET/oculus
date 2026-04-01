import {type Feature, useFeaturesStore} from "../../store/useFeaturesStore";
import FeatureCard from "./features/FeatureCard";

export default function FeaturesTab() {
    const {features} = useFeaturesStore();

    if (!features.length) {
        return <div className="text-center py-5">No features loaded</div>;
    }

    return (
        <div className="features-list">
            {features.map((f: Feature) => (
                <FeatureCard key={f.id} feature={f} />
            ))}
        </div>
    );
}