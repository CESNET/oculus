import L from 'leaflet';
import type { LatLngExpression } from 'leaflet';

export function toLatLngTuple(expr: LatLngExpression): [number, number] {
    const latLng = L.latLng(expr);
    return [latLng.lat, latLng.lng];
}
