import {type Feature, useFeaturesStore} from "../../../store/useFeaturesStore.ts";
import {useState} from "react";
import {useLoadingStore} from "../../../store/useLoadingStore.ts";
import {requestVisualization} from "../../../api/backend/requestVisualization.ts";

interface FeatureCardProps {
    feature: Feature;
}

const FeatureCard: React.FC<FeatureCardProps> = ({feature}) => {
    const setHoveredId = useFeaturesStore(state => state.setHoveredFeatureId);

    const [copied, setUrlCopied] = useState(false);

    const handleUrlCopy = () => {
        navigator.clipboard.writeText(feature.productUrl).then(() => {
            setUrlCopied(true);
            setTimeout(() => setUrlCopied(false), 2000);
        });
    };

    const handleVisualize = async () => {
        const { startLoading, stopLoading } = useLoadingStore.getState();
        const controller = startLoading();

        try {
            const { job_id, processed_files } = await requestVisualization(feature, {
                signal: controller.signal,
                //onMessage: (status) => console.log("Job status:", status),
            });

            console.log("Visualization finished!", job_id, processed_files);

        } catch (err: any) {
            if (err.name === "AbortError") {
                console.log("Visualization aborted by user");
            } else {
                console.error("Error during visualization:", err);
            }
        } finally {
            stopLoading(); // zakryje overlay
        }
    };

    return (
        <div
            className="card h-100 shadow-sm feature-card"
            onMouseEnter={() => setHoveredId(feature.id)}
            onMouseLeave={() => setHoveredId(null)}
        >
            <div className="card-body d-flex flex-column">
                <h5 className="card-title">{feature.title}</h5>
                <p className="card-text mb-1"><strong>Platform:</strong> {feature.platform}</p>
                <p className="card-text mb-3"><strong>Date:</strong> {feature.acquisitionDate}</p>

                <button className="btn btn-primary mb-2" onClick={handleVisualize}>
                    Visualize
                </button>

                <div className="d-flex gap-2">
                    <a
                        href={feature.productUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-outline-secondary btn-sm flex-grow-1"
                    >
                        Open Product Page
                    </a>

                    <button
                        className="btn btn-outline-info btn-sm"
                        onClick={handleUrlCopy}
                        title="Copy Product URL"
                    >
                        <i className={`bi ${copied ? "bi-check" : "bi-clipboard"}`} />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default FeatureCard;