import {useVisualizationStore} from "../../store/useVisualizationStore";
import ProcessedFileCard from "./visualization/ProcessedFileCard";

export default function VisualizationTab() {
    const {
        processedFiles,
        tileLayers,
        selectedTileLayerIndex,
        setSelectedTileLayerIndex,
        opacity,
        setOpacity,
    } = useVisualizationStore();

    const hasLayers = tileLayers.length > 0;
    const hasFiles = processedFiles.length > 0;

    if (!hasLayers && !hasFiles) {
        return <div className="text-center py-5">No visualization data</div>;
    }

    return (
        <>
            {/* =========================
                TILE LAYERS
               ========================= */}
            {hasLayers && (
                <div className="filter-section">
                    <h3>Visualization Settings</h3>

                    <label htmlFor="tileLayerSelect">
                        Active Tile Layer
                    </label>

                    <select
                        id="tileLayerSelect"
                        value={selectedTileLayerIndex ?? ""}
                        onChange={(e) =>
                            setSelectedTileLayerIndex(Number(e.target.value))
                        }
                    >
                        {tileLayers.map((tile, idx) => (
                            <option key={idx} value={idx}>
                                {tile.name} ({tile.format.toUpperCase()})
                            </option>
                        ))}
                    </select>

                    <label style={{marginTop: "1rem"}}>
                        Layer Opacity
                    </label>

                    <div className="opacity-control">
                        <input
                            type="range"
                            min={0}
                            max={1}
                            step={0.01}
                            value={opacity}
                            onChange={(e) => setOpacity(Number(e.target.value))}
                        />

                        <span className="opacity-value">
                            {Math.round(opacity * 100)}%
                        </span>
                    </div>
                </div>
            )}

            {/* =========================
                PROCESSED FILES
               ========================= */}
            {hasFiles && (
                <div className="filter-section">
                    <h3>Processed Files</h3>

                    <div className="processed-files-list">
                        {processedFiles.map((file) => (
                            <ProcessedFileCard key={file.path} file={file} />
                        ))}
                    </div>
                </div>
            )}
        </>
    );
}