import { useVisualizationStore } from "../../store/useVisualizationStore";
import ProcessedFileCard from "./visualization/ProcessedFileCard";

export default function VisualizeTab() {
    const {
        processedFiles,
        tileLayers,
        selectedTileLayerIndex,
        setSelectedTileLayerIndex,
        opacity,
        setOpacity
    } = useVisualizationStore();

    if (!processedFiles.length && !tileLayers.length) {
        return <div className="sidebar-panel">No visualization data available</div>;
    }

    return (
        <div className="sidebar-panel">
            {tileLayers.length > 0 && (
                <div className="filter-section">
                    <h3>Visualization Settings</h3>

                    <label htmlFor="tileLayerSelect">Active Tile Layer</label>
                    <select
                        id="tileLayerSelect"
                        value={selectedTileLayerIndex ?? ""}
                        onChange={(e) => setSelectedTileLayerIndex(Number(e.target.value))}
                    >
                        {tileLayers.map((tile, idx) => (
                            <option key={idx} value={idx}>
                                {tile.name} ({tile.format.toUpperCase()})
                            </option>
                        ))}
                    </select>

                    <label htmlFor="opacityRange" style={{ marginTop: '1rem', display: 'block' }}>
                        Layer Opacity
                    </label>
                    <div className="viz-opacity-wrapper">
                        <input
                            id="opacityRange"
                            type="range"
                            min={0}
                            max={1}
                            step={0.01}
                            value={opacity}
                            onChange={(e) => setOpacity(Number(e.target.value))}
                        />
                        <span className="opacity-number">{Math.round(opacity * 100)} %</span>
                    </div>
                </div>
            )}

            {processedFiles.length > 0 && (
                <div className="filter-section" style={{ borderBottom: 'none' }}>
                    <h3>Processed Files</h3>
                    <div className="processed-files-list">
                        {processedFiles.map((file) => (
                            <ProcessedFileCard key={file.path} file={file} />
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}