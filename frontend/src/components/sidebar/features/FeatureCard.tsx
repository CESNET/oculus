import {useState} from "react";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Tooltip from "react-bootstrap/Tooltip";

import {useFeaturesStore} from "../../../store/useFeaturesStore";
import type {Feature} from "../../../types/feature.ts";
import RunVisualizationButton from "../visualization/RunVisualizationButton.tsx";

interface FeatureCardProps {
    feature: Feature;
}

export default function FeatureCard({feature}: FeatureCardProps) {
    const setHoveredId = useFeaturesStore(
        (state) => state.setHoveredFeatureId
    );

    const [copiedName, setCopiedName] = useState(false);
    const [copiedId, setCopiedId] = useState(false);
    const [copiedUrl, setCopiedUrl] = useState(false);

    /*
    // Not really sure why I was resetting Sentinel2Bands, handleVisualization() was executed only from FeatureCard
    const handleVisualization = async (feature: Feature) => {
        useVisualizationStore.getState().resetSentinel2Bands(true)
        await runVisualization(feature);
    }
     */

    const handleCopy = async (
        value: string,
        setCopied: (copied: boolean) => void
    ) => {
        try {
            await navigator.clipboard.writeText(value);
            setCopied(true);

            window.setTimeout(() => {
                setCopied(false);
            }, 2000);
        } catch (error) {
            console.error("Failed to copy to clipboard:", error);
        }
    };

    const formattedDateTime = new Intl.DateTimeFormat(undefined, {
        dateStyle: "medium",
        timeStyle: "medium",
    }).format(new Date(feature.acquisitionDateTime));

    return (
        <div
            className="card h-100 shadow-sm feature-card"
            onMouseEnter={() => setHoveredId(feature.id)}
            onMouseLeave={() => setHoveredId(null)}
        >
            <div className="card-body d-flex flex-column">
                <h5 className="card-title">{feature.title}</h5>

                <p className="card-text metadata-row metadata-row--date">
                    <span className="metadata-label">Date:</span>
                    <span className="metadata-value">
                        {formattedDateTime}
                    </span>
                </p>

                <p className="card-text metadata-row">
                    <span className="metadata-label">Name:</span>

                    <OverlayTrigger
                        placement="top"
                        overlay={
                            <Tooltip>
                                {copiedName ? (
                                    <small>Copied to clipboard</small>
                                ) : (
                                    <>
                                        <code>{feature.name}</code>
                                        <hr className="my-1" />
                                        <small>Click to copy</small>
                                    </>
                                )}
                            </Tooltip>
                        }
                    >
                        <span
                            className="metadata-value metadata-copyable feature-name"
                            onClick={() =>
                                handleCopy(feature.name, setCopiedName)
                            }
                            title={feature.name}
                        >
                            {feature.name}
                        </span>
                    </OverlayTrigger>
                </p>

                <p className="card-text metadata-row metadata-row--id">
                    <span className="metadata-label">ID:</span>

                    <OverlayTrigger
                        placement="top"
                        overlay={
                            <Tooltip>
                                {copiedId ? (
                                    <small>Copied to clipboard</small>
                                ) : (
                                    <>
                                        <code>{feature.id}</code>
                                        <hr className="my-1" />
                                        <small>Click to copy</small>
                                    </>
                                )}
                            </Tooltip>
                        }
                    >
                        <span
                            className="metadata-value metadata-copyable feature-id"
                            onClick={() =>
                                handleCopy(feature.id, setCopiedId)
                            }
                            title={feature.id}
                        >
                            {feature.id}
                        </span>
                    </OverlayTrigger>
                </p>

                <RunVisualizationButton featureId={feature.id} />

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
                        type="button"
                        className="btn btn-outline-secondary btn-sm"
                        onClick={() =>
                            handleCopy(feature.productUrl, setCopiedUrl)
                        }
                        title="Copy product URL"
                        aria-label="Copy product URL"
                    >
                        <i
                            className={`bi ${
                                copiedUrl ? "bi-check" : "bi-clipboard"
                            }`}
                        />
                    </button>
                </div>
            </div>
        </div>
    );
}
