import {Dataset, DatasetFamily, DatasetToFamily} from "../types/datasets";
import {type ProductFile, type TileLayer, useVisualizationStore} from "../store/useVisualizationStore";
import type {Feature} from "../store/useFeaturesStore";
import {useFiltersStore} from "../store/useFiltersStore";
import {bandsToApi, levelsToApi} from "./filterUtils.ts";

export const applyVisualizationResults = (
    processed_files: string[],
    outputs: Record<string, { product: boolean; tiles?: boolean }>
) => {
    const newProcessedFiles: ProductFile[] = [];
    const newTileLayers: TileLayer[] = [];

    processed_files.forEach((path) => {
        const baseName = path.split("/").pop()!;
        Object.entries(outputs).forEach(([format, info]) => {
            if (info.product) newProcessedFiles.push({path, name: baseName, format});
            if (info.tiles) newTileLayers.push({path, name: baseName, format});
        });
    });

    const visualizationStore = useVisualizationStore.getState();
    visualizationStore.setProcessedFiles(newProcessedFiles);
    visualizationStore.setTileLayers(newTileLayers);
    visualizationStore.setSelectedTileLayerIndex(newTileLayers.length ? 0 : null);
};

/**
 * Vytvoří payload pro backend visualizace.
 * @param feature - feature, kterou chceme vizualizovat
 * @param outputs - aktuální nastavení výstupních formátů (jpg/png/webp)
 */
export const visualizeFeature = (feature: Feature) => {
    const outputs = useVisualizationStore.getState().outputs;

    const payload: any = {
        dataset: feature.dataset,
        properties: {
            quality: 80,
            zoom_levels: [8, 9, 10, 11, 12, 13, 14], // TODO Zoom levels by se asi měly počítat na backendu, tohle by měl být override, ale ne defaultně posílané
            outputs,
        }
    };

    // metadata podle dataset family
    switch (DatasetToFamily[feature.dataset]) {
        case DatasetFamily.Sentinel:
            payload.metadata = {"sentinel:feature_id": feature.id};
            break;
        case DatasetFamily.Landsat:
            payload.metadata = {"landsat:feature_id": feature.id};
            break;
        default:
            throw new Error("Unknown dataset family for dataset: " + feature.dataset);
    }

    // dataset-specific properties
    switch (feature.dataset) {
        case Dataset.Sentinel1:
            payload.properties = {
                ...payload.properties,
                ...visualizeSentinel1(feature)
            };
            break;
        case Dataset.Sentinel2:
            payload.properties = {
                ...payload.properties,
                ...visualizeSentinel2(feature)
            };
            break;
        case Dataset.Landsat:
            payload.properties = {
                ...payload.properties,
                ...visualizeLandsat(feature)
            };
            break;
        default:
            throw new Error("Dataset visualization not implemented: " + feature.dataset);
    }

    return payload;
};

// ---------------- Sentinel-1 ----------------
const visualizeSentinel1 = (feature: Feature) => {
    const filters = useFiltersStore.getState().sentinel1;

    if (!filters.levels.length) throw new Error("Sentinel-1 filters missing levels");
    if (!filters.productTypes.length) throw new Error("Sentinel-1 filters missing productTypes");
    if (!filters.operationalModes.length) throw new Error("Sentinel-1 filters missing operationalModes");
    if (!filters.polarizations.length) throw new Error("Sentinel-1 filters missing polarizations");
    if (!feature.platform) throw new Error("Feature missing platform");

    return {
        platform: feature.platform,
        filters: {
            levels: levelsToApi(feature.dataset, filters.levels),
            product_types: filters.productTypes,
            operational_modes: filters.operationalModes,
            polarisation_channels: filters.polarizations
        }
    };
};

// ---------------- Sentinel-2 ----------------
const visualizeSentinel2 = (feature: Feature) => {
    const filters = useFiltersStore.getState().sentinel2;

    if (filters.cloudCover == null) throw new Error("Sentinel-2 filters missing cloudCover");
    if (!filters.levels.length) throw new Error("Sentinel-2 filters missing levels");
    if (!filters.bands.length) throw new Error("Sentinel-2 filters missing bands");
    if (!feature.platform) throw new Error("Feature missing platform");

    return {
        platform: feature.platform,
        filters: {
            cloud_cover: filters.cloudCover,
            levels: levelsToApi(feature.dataset, filters.levels),
            bands: bandsToApi(feature.dataset, filters.bands)
        }
    };
};

// ---------------- Landsat ----------------
const visualizeLandsat = (feature: Feature) => {
    throw new Error("Dataset visualization not implemented: " + feature.dataset);
    return {};
};