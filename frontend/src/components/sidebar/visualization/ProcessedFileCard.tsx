import type {ProductFile} from "../../../store/useVisualizationStore";

/**
 * ProcessedFileCard
 * Displays processed file metadata in unified sidebar card system.
 */
type Props = {
    file: ProductFile;
};

export default function ProcessedFileCard({file}: Props) {
    const fullPath = `${file.path}.${file.format}`;

    return (
        <div className="card feature-card processed-file-card">
            <div className="card-body">

                <h5
                    className="card-title"
                    title={`${file.name}.${file.format}`}
                >
                    {file.name}.{file.format}
                </h5>

                {/*
                <p className="card-text">
                    <strong>Format:</strong> {file.format}
                </p>
                */}

                {/*
                <p className="card-text">
                    <strong>Path:</strong> {file.path}
                </p>
                */}

                <div className="d-flex gap-2 mt-auto">
                    <a
                        href={fullPath}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-outline-secondary btn-sm flex-fill"
                        title="Open file in new tab"
                    >
                        <i className="bi bi-box-arrow-up-right" />
                    </a>

                    <a
                        href={fullPath}
                        download
                        className="btn btn-outline-secondary btn-sm flex-fill"
                        title="Download file"
                    >
                        <i className="bi bi-download" />
                    </a>

                    <button
                        className="btn btn-outline-secondary btn-sm flex-fill"
                        onClick={
                            () => {
                                const fullUrl = new URL(fullPath, window.location.origin).href;
                                navigator.clipboard.writeText(fullUrl)
                            }
                        }
                        title="Copy link"
                    >
                        <i className="bi bi-clipboard" />
                    </button>
                </div>
            </div>
        </div>
    );
}