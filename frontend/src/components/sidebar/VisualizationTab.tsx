import {useMemo} from "react";

import {useVisualizationStore} from "../../store/useVisualizationStore";
import type {Sentinel2VisualizationState} from "../../store/useVisualizationStore";
import {useFiltersStore} from "../../store/useFiltersStore";
import {useFeaturesStore} from "../../store/useFeaturesStore";

import {Dataset} from "../../types/datasets";

import {getAllVisualizationOptions, getProductFiles, getTileLayers} from "../../utils/visualizationUtils";
import {runVisualization} from "../../service/visualizationService";

import ProcessedFileCard from "./visualization/ProcessedFileCard";
import MultiButtonGroup from "./MultiButtonGroup.tsx";

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
        featureId,
        processedFiles,
        selectedTileLayerPath,
        setSelectedTileLayerPath,
        opacity,
        setOpacity,
        sentinel2,
        toggleSentinel2Band,
    } = useVisualizationStore();


    const feature = useFeaturesStore(
        s => featureId ? s.featuresById[featureId] : undefined
    );


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


    const sentinel2Defaults = getAllVisualizationOptions(Dataset.Sentinel2) as Sentinel2VisualizationState;

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
                        Visualization Settings
                    </h3>


                    {dataset === Dataset.Sentinel2 && (
                        <MultiButtonGroup
                            label="Bands"
                            values={sentinel2Defaults.bands}
                            selected={sentinel2.bands}
                            onToggle={toggleSentinel2Band}
                        />
                    )}

                    <button
                        className="btn btn-primary mb-3"
                        disabled={!feature}
                        onClick={() => {
                            if (feature) {
                                runVisualization(feature);
                            }
                        }}
                    >
                        Re-render Visualization
                    </button>

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