import { useFeaturesStore } from "../../store/useFeaturesStore";

export default function FeaturesTab() {
    const { features } = useFeaturesStore();

    if (!features.length) {
        return <div>No features loaded</div>;
    }



    return (
        <div>
            {features.map((f) => (
                <div key={f.id} className="feature-tile">
                    <strong>{f.title}</strong>

                    <div>Platform: {f.platform}</div>
                    <div>Date: {f.acquisitionDate}</div>

                    <a href={f.productUrl} target="_blank">
                        Open
                    </a>
                </div>
            ))}
        </div>
    );
}