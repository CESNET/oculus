import {useMemo} from "react";

import {useVisualizationStore} from "../../store/useVisualizationStore";

import {useFiltersStore} from "../../store/useFiltersStore";

import {Dataset} from "../../types/datasets";

import {getProductFiles, getTileLayers} from "../../utils/visualizationUtils";

import ProcessedFileCard from "./visualization/ProcessedFileCard";
import Sentinel2VisualizationOptions from "./visualization/Sentinel2VisualizationOptions";

function compareNameAndFormat(
    a: { name: string; format: string },
    b: { name: string; format: string }
) {
    const formatCompare = a.format.localeCompare(b.format);

    if (formatCompare !== 0) {
        return formatCompare;
    }

    return a.name.localeCompare(b.name, undefined, {
        numeric: true,
    });
}

export default function VisualizationTab() {
    const dataset = useFiltersStore((s) => s.dataset);

    const {
        //featureId,
        processedFiles,
        selectedTileLayerPath,
        setSelectedTileLayerPath,
        opacity,
        setOpacity,
    } = useVisualizationStore();

    /*
    const feature = useFeaturesStore(
        s => featureId ? s.featuresById[featureId] : undefined
    );
     */


    /**
     * Derived data
     */
    const tileLayers = useMemo(
        () => getTileLayers(processedFiles), [processedFiles]
    );


    const productFiles = useMemo(
        () => getProductFiles(processedFiles), [processedFiles]
    );

    const hasLayers = tileLayers.length > 0;
    const hasFiles = productFiles.length > 0;

    const sortedTileLayers = useMemo(
        () => [...tileLayers].sort(compareNameAndFormat), [tileLayers]
    );


    const sortedProcessedFiles = useMemo(
        () => [...productFiles].sort(compareNameAndFormat), [productFiles]
    );


    if (!hasLayers && !hasFiles) {
        return (
            <div className="text-center py-5">
                No visualization data
            </div>
        );
    }

    return (
        <>
            {/* =========================
                VISUALIZATION SETTINGS
               ========================= */}

            {hasLayers && (
                <div className="filter-section">

                    <h3>
                        Visualization options
                    </h3>


                    {dataset === Dataset.Sentinel2 && (
                        <Sentinel2VisualizationOptions />
                    )}

                    <label htmlFor="tileLayerSelect">
                        Active Tile Layer
                    </label>

                    <select
                        id="tileLayerSelect"
                        value={selectedTileLayerPath ?? ""}
                        onChange={(e) =>
                            setSelectedTileLayerPath(e.target.value || null)
                        }
                    >
                        {sortedTileLayers.map(
                            tile => (
                                <option
                                    key={`${tile.path}`}
                                    value={tile.path}
                                >
                                    {tile.name.toUpperCase()}.{tile.format.toUpperCase()}
                                </option>
                            )
                        )}
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
                            onChange={(e) =>
                                setOpacity(Number(e.target.value))
                            }
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
                    <h3>
                        Processed Files
                    </h3>

                    <div className="processed-files-list">
                        {sortedProcessedFiles.map(
                            file => (
                                <ProcessedFileCard
                                    key={file.path}
                                    file={file}
                                />
                            )
                        )}
                    </div>
                </div>
            )}
        </>
    );
}