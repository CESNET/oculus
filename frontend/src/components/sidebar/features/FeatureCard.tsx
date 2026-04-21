import {type Feature, useFeaturesStore} from "../../../store/useFeaturesStore.ts";
import {useVisualizationStore} from "../../../store/useVisualizationStore.ts";
import {useSidebarStore} from "../../../store/useSidebarStore.ts";
import {useState} from "react";
import {useLoadingStore} from "../../../store/useLoadingStore.ts";
import {requestVisualization} from "../../../api/backend/requestVisualization.ts";
import {applyVisualizationResults} from "../../../utils/featureUtils.ts";

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
        const {startLoading, stopLoading} = useLoadingStore.getState();
        const controller = startLoading();

        try {
            const {job_id, processed_files, available_zoom_levels} = await requestVisualization(feature, {
                signal: controller.signal,
                onMessage: (status) => console.log("Job status:", status)
            });

            useVisualizationStore.getState().setJobId(job_id);
            useVisualizationStore.getState().setFeatureId(feature.id);

            applyVisualizationResults(
                processed_files,
                available_zoom_levels,
                useVisualizationStore.getState().outputs
            );
            useSidebarStore.getState().setActiveTab(2);

        } catch (err: any) {
            if (err.name === "AbortError") console.log("Visualization aborted");
            else console.error("Error during visualization:", err);

        } finally {
            stopLoading();
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
                <p className="card-text mb-1"><strong>Platform:</strong>&nbsp;{feature.platform}</p>
                <p className="card-text mb-1"><strong>Date:</strong>&nbsp;{feature.acquisitionDate}</p>
                <p className="card-text mb-3"><strong>ID:</strong>&nbsp;{feature.id}</p>

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
                        Open product page
                    </a>

                    <button
                        className="btn btn-outline-secondary btn-sm btn-sm"
                        onClick={handleUrlCopy}
                        title="Copy product URL"
                    >
                        <i className={`bi ${copied ? "bi-check" : "bi-clipboard"}`} />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default FeatureCard;