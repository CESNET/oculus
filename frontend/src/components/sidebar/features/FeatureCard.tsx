import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Tooltip from "react-bootstrap/Tooltip";

import {useFeaturesStore} from "../../../store/useFeaturesStore";
import {useState} from "react";
import {runVisualization} from "../../../service/visualizationService";
import {useVisualizationStore} from "../../../store/useVisualizationStore.ts";
import type {Feature} from "../../../types/feature.ts";

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

    const handleVisualization = async (feature: Feature) => {
        useVisualizationStore.getState().resetSentinel2Bands(true)
        await runVisualization(feature);
    }

    const handleCopyId = async () => {
        await navigator.clipboard.writeText(feature.id);

        setCopiedId(true);

        setTimeout(() => {
            setCopiedId(false);
        }, 2000);
    };

    const handleCopyName = async () => {
        await navigator.clipboard.writeText(feature.name);

        setCopiedName(true);

        setTimeout(() => {
            setCopiedName(false);
        }, 2000);
    };

    const handleCopyUrl = async () => {
        await navigator.clipboard.writeText(feature.productUrl);

        setCopiedUrl(true);

        setTimeout(() => {
            setCopiedUrl(false);
        }, 2000);
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

                <p className="card-text mb-1">
                    <strong>Date:</strong>&nbsp;{formattedDateTime}
                </p>

                <p className="card-text mb-1 d-flex">
                    <strong className="me-2">Name:</strong>

                    <OverlayTrigger
                        placement="top"
                        overlay={
                            <Tooltip>
                                {
                                    copiedName
                                        ? (<small>Copied to clipboard</small>)
                                        : (
                                            <>
                                                <code>{feature.name}</code>

                                                <hr className="my-1" />

                                                <small>Click to copy</small>
                                            </>
                                        )
                                }
                            </Tooltip>
                        }
                    >
                        <span
                            className="feature-name"
                            onClick={handleCopyName}
                            style={{cursor: "pointer"}}
                        >
                            <u>{feature.name}</u>
                        </span>
                    </OverlayTrigger>
                </p>

                <p className="card-text mb-3 d-flex">
                    <strong className="me-2">ID:</strong>

                    <OverlayTrigger
                        placement="top"
                        overlay={
                            <Tooltip>
                                {
                                    copiedId
                                        ? (<small>Copied to clipboard</small>)
                                        : (
                                            <>
                                                <code>{feature.id}</code>

                                                <hr className="my-1" />

                                                <small>Click to copy</small>
                                            </>
                                        )
                                }
                            </Tooltip>
                        }
                    >
                        <span
                            className="feature-id"
                            onClick={handleCopyId}
                            style={{cursor: "pointer"}}
                        >
                            <u>{feature.id}</u>
                        </span>
                    </OverlayTrigger>
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
                        <i className={`bi ${copiedUrl ? "bi-check" : "bi-clipboard"}`} />
                    </button>
                </div>
            </div>
        </div>
    );
}