import L from 'leaflet';
import type { LatLngExpression } from 'leaflet';
import { useMapStore } from '../store/useMapStore';

export function toLatLngTuple(expr: LatLngExpression): [number, number] {
    const latLng = L.latLng(expr);
    return [latLng.lat, latLng.lng];
}

let mapInstance: L.Map | null = null;

/**
 * Registrace Leaflet map instance
 */
export function registerMap(map: L.Map) {
    mapInstance = map;
}


/**
 * Jednotné API pro pohyb mapy
 */
export function moveMap(
    center: LatLngExpression,
    zoom?: number,
    options?: any
) {
    if (!mapInstance) return;

    const target = center as [number, number];

    if (zoom !== undefined) {
        mapInstance.flyTo(target, zoom, options);
    } else {
        mapInstance.panTo(target, options);
    }

    const currentZoom = mapInstance.getZoom();
    useMapStore.getState().setView(target, zoom ?? currentZoom);
}

export async function searchLocation(query: string) {
    if (!query) return [];

    try {
        const res = await fetch(
            `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`,
            {
                headers: {
                    "User-Agent": "CESNET-Oculus-Visualizer/1.0",
                },
            }
        );

        const data = await res.json();

        return data.sort((a: any, b: any) => {
            const rankDiff = (b.place_rank || 0) - (a.place_rank || 0);
            if (rankDiff !== 0) return rankDiff;
            return (b.importance || 0) - (a.importance || 0);
        });
    } catch (err) {
        console.error("searchLocation error:", err);
        return [];
    }
}