import type { ProductFile } from "../../../store/useVisualizationStore.ts";

type Props = {
    file: ProductFile;
};

export default function ProcessedFileCard({ file }: Props) {
    const fullPath = `${file.path}.${file.format}`;

    return (
        <div className="card h-100 shadow-sm feature-card processed-file-card">
            <div className="card-body d-flex flex-column">
                <h5 className="card-title text-truncate" title={`${file.name}.${file.format}`}>
                    {file.name}.{file.format}
                </h5>

                <p className="card-text mb-1 text-truncate">
                    <strong>Format:</strong> {file.format}
                </p>

                <p className="card-text mb-3 file-path">
                    <strong>Path:</strong> {file.path}
                </p>

                <div className="d-flex gap-2 mt-auto">
                    <a
                        href={fullPath}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-outline-secondary btn-sm flex-grow-1"
                        title={fullPath}
                    >
                        Download
                    </a>

                    <button
                        className="btn btn-outline-secondary btn-sm"
                        onClick={() => navigator.clipboard.writeText(fullPath)}
                        title="Copy full path"
                    >
                        <i className="bi bi-clipboard" />
                    </button>
                </div>
            </div>
        </div>
    );
}