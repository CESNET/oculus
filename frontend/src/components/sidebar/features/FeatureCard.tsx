import type { Feature } from "../../../store/useFeaturesStore.ts";
import { useState } from "react";

interface FeatureCardProps {
    feature: Feature;
}

const FeatureCard: React.FC<FeatureCardProps> = ({ feature }) => {
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(feature.productUrl).then(() => {
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        });
    };

    const handleVisualize = () => {
        alert(`Visualizing feature ${feature.title}`);
        // TODO volat backend
    };

    return (
        <div className="card h-100 shadow-sm feature-card">
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
                        onClick={handleCopy}
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