import React, { useEffect } from 'react';
import {
    MapContainer,
    TileLayer,
    useMapEvents,
    useMap,
    Polygon
} from 'react-leaflet';

import { useMapStore } from '../../store/useMapStore';
import { useFiltersStore } from '../../store/useFiltersStore';
import { useFeaturesStore } from "../../store/useFeaturesStore";
import UserLocationMarker from './UserLocationMarker';
import LocateButton from './LocateButton';
import ProductLayer from './layers/ProductLayer';
import type { LatLngExpression } from 'leaflet';
import { useVisualizationStore } from "../../store/useVisualizationStore";
import { registerMap } from '../../utils/mapUtils';

interface Props {
    center: LatLngExpression;
    zoom: number;
    location?: { lat: number; lng: number };
    userLocation?: boolean;
    loadingLocation?: boolean;
    productUrl?: string;
    programmaticRef: React.MutableRefObject<boolean>;
}

/**
 * Registrace Leaflet instance
 */
const MapRegistrar = () => {
    const map = useMap();

    useEffect(() => {
        registerMap(map);
    }, [map]);

    return null;
};

/**
 * Sync zoom + bbox
 */
const MapUpdater = ({ programmaticRef }: any) => {
    const setView = useMapStore(state => state.setView);
    const setBboxFromMap = useFiltersStore(state => state.setBboxFromMap);

    const map = useMapEvents({
        moveend: () => {
            const center = map.getCenter();
            const zoom = map.getZoom();
            const bounds = map.getBounds();

            setView([center.lat, center.lng], zoom);

            if (programmaticRef.current) {
                programmaticRef.current = false;
                return;
            }

            setBboxFromMap(
                bounds.getNorth(),
                bounds.getSouth(),
                bounds.getEast(),
                bounds.getWest()
            );
        }
    });

    useEffect(() => {
        const bounds = map.getBounds();

        setBboxFromMap(
            bounds.getNorth(),
            bounds.getSouth(),
            bounds.getEast(),
            bounds.getWest()
        );
    }, [map, setBboxFromMap]);

    return null;
};

const Map: React.FC<Props> = ({
                                  center,
                                  zoom,
                                  location,
                                  userLocation,
                                  loadingLocation,
                                  productUrl,
                                  programmaticRef
                              }) => {

    const hoveredId = useFeaturesStore(state => state.hoveredFeatureId);
    const hoveredFeature = useFeaturesStore(state =>
        state.features.find(f => f.id === hoveredId)
    );

    const { tileLayers, selectedTileLayerIndex, opacity } = useVisualizationStore();

    const selectedTile =
        selectedTileLayerIndex !== null
            ? tileLayers[selectedTileLayerIndex]
            : null;

    return (
        <MapContainer center={center} zoom={zoom} className="w-100 h-100">

            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="&copy; OpenStreetMap contributors"
            />

            {hoveredFeature && (
                <Polygon
                    positions={hoveredFeature.geometry.coordinates}
                    pathOptions={{
                        color: 'gray',
                        fillColor: 'gray',
                        fillOpacity: 0.3,
                        weight: 3
                    }}
                />
            )}

            {userLocation && (
                <LocateButton
                    lat={location?.lat ?? 0}
                    lng={location?.lng ?? 0}
                    zoom={13}
                    userLocation={!!userLocation}
                    loading={loadingLocation ?? false}
                    programmaticRef={programmaticRef}
                />
            )}

            {userLocation && location && (
                <UserLocationMarker location={location} />
            )}

            {productUrl && (
                <ProductLayer productUrl={productUrl} opacity={1} />
            )}

            {selectedTile && (
                <TileLayer
                    url={`${selectedTile.path}/{z}/{x}/{y}.${selectedTile.format}`}
                    opacity={opacity}
                />
            )}

            <MapRegistrar />
            <MapUpdater programmaticRef={programmaticRef} />
        </MapContainer>
    );
};

export default Map;