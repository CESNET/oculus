import type {Feature} from "../../../store/useFeaturesStore.ts";
import {Dataset} from "../../../types/datasets.ts"; // Importuj svůj enum

/**
 * Parsování WKT na souřadnice (zůstává stejné)
 */
const parseWKTToCoordinates = (wkt: string): [number, number][] => {
    try {
        const match = wkt.match(/\(\((.*)\)\)/);
        if (!match) return [];
        const points = match[1].split(",");
        return points.map(point => {
            const [lng, lat] = point.trim().split(/\s+/).map(Number);
            return [lat, lng];
        });
    } catch (e) {
        return [];
    }
};

/**
 * Optimalizovaný mapper s rozlišením datasetu
 */
export const mapCDSEToFeature = (item: any, dataset: Dataset): Feature => {
    const id = item.Id;

    return {
        id: id,
        title: item.Name,
        // Pokud API nevrátí název kolekce, použijeme přímo hodnotu z našeho Dataset "enumu"
        platform: item.Collection?.Name ?? dataset,
        acquisitionDate: item.ContentDate?.Start ?? "",
        productUrl: `https://catalogue.dataspace.copernicus.eu/odata/v1/Products(${id})`,
        dataset,
        geometry: {
            type: "Polygon",
            coordinates: item.Footprint
                ? [parseWKTToCoordinates(item.Footprint)]
                : []
        },
    };
};