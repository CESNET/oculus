import { type Feature, useFeaturesStore } from "../../../store/useFeaturesStore";
import { useState } from "react";
import { runVisualization } from "../../../service/visualizationService";
import {useVisualizationStore} from "../../../store/useVisualizationStore.ts";

interface FeatureCardProps {
    feature: Feature;
}

export default function FeatureCard({ feature }: FeatureCardProps) {
    const setHoveredId = useFeaturesStore(
        (state) => state.setHoveredFeatureId
    );

    const [copied, setCopied] = useState(false);

    const handleVisualization = async (feature: Feature) => {
        useVisualizationStore.getState().resetSentinel2Bands(true)
        await runVisualization(feature);
    }

    const handleCopyUrl = async () => {
        await navigator.clipboard.writeText(feature.productUrl);

        setCopied(true);

        setTimeout(() => {
            setCopied(false);
        }, 2000);
    };

    return (
        <div
            className="card h-100 shadow-sm feature-card"
            onMouseEnter={() => setHoveredId(feature.id)}
            onMouseLeave={() => setHoveredId(null)}
        >
            <div className="card-body d-flex flex-column">
                <h5 className="card-title">{feature.title}</h5>

                <p className="card-text mb-1">
                    <strong>Platform:</strong>&nbsp;{feature.platform}
                </p>

                <p className="card-text mb-1">
                    <strong>Date:</strong>&nbsp;{feature.acquisitionDate}
                </p>

                <p className="card-text mb-3">
                    <strong>ID:</strong>&nbsp;{feature.id}
                </p>

                <button
                    className="btn btn-primary mb-2"
                    onClick={() => handleVisualization(feature)}
                >
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
                        className="btn btn-outline-secondary btn-sm"
                        onClick={handleCopyUrl}
                        title="Copy product URL"
                    >
                        <i className={`bi ${copied ? "bi-check" : "bi-clipboard"}`} />
                    </button>
                </div>
            </div>
        </div>
    );
}