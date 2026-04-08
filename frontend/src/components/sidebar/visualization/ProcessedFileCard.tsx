import type { ProductFile } from "../../../store/useVisualizationStore.ts";

type Props = {
    file: ProductFile;
};

export default function ProcessedFileCard({ file }: Props) {
    const fullPath = `${file.path}.${file.format}`;

    return (
        <a
            href={fullPath}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-outline-secondary processed-file-card"
        >
            <span className="file-name">Download {file.name}.{file.format}</span>
            <span className="file-path" title={fullPath}>
                {fullPath}
            </span>
        </a>
    );
}