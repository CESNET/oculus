import L from 'leaflet';
import type {LatLngExpression} from 'leaflet';
import {useMapStore} from '../store/useMapStore';

export function toLatLngTuple(expr: LatLngExpression): [number, number] {
    const latLng = L.latLng(expr);
    return [latLng.lat, latLng.lng];
}

/**
 * Fetch výsledků z Nominatim podle query
 */
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

        // seřadíme podle place_rank a importance, aby byly relevantní výsledky nahoře
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

/**
 * Posune mapu na konkrétní souřadnice a vrátí data pro marker
 */
export function goToLocation(
    lat: number,
    lon: number,
    programmaticRef: React.MutableRefObject<boolean>
) {
    // Označíme posun jako programový
    programmaticRef.current = true;

    // Posun mapy přes zustand store
    useMapStore.getState().setView([lat, lon], useMapStore.getState().zoom);

    // Vracíme data pro marker
    return {lat, lon};
}