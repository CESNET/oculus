import {create} from 'zustand';
import type {LatLngExpression} from 'leaflet';

interface MapState {
    center: LatLngExpression;
    zoom: number;
    setView: (center: LatLngExpression, zoom: number) => void;
}

export const useMapStore = create<MapState>((set) => ({
    center: [50.08804, 14.42076], // default Praha
    zoom: 13,
    setView: (center, zoom) => set({center, zoom}),
}));