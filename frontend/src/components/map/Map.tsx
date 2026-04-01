import React, {useEffect} from 'react';
import {MapContainer, TileLayer, useMapEvents, Polygon} from 'react-leaflet';
import {useMapStore} from '../../store/useMapStore';
import {useFiltersStore} from '../../store/useFiltersStore';
import {useFeaturesStore} from "../../store/useFeaturesStore.ts";
import UserLocationMarker from './UserLocationMarker';
import LocateButton from './LocateButton';
import ProductLayer from './layers/ProductLayer';
import type {LatLngExpression} from 'leaflet';


interface Props {
    center: LatLngExpression;
    zoom: number;
    location?: { lat: number; lng: number };
    userLocation?: boolean;
    loadingLocation?: boolean;
    productUrl?: string;
    programmaticRef: React.MutableRefObject<boolean>;
}

const MapUpdater = ({programmaticRef}: { programmaticRef: React.MutableRefObject<boolean> }) => {
    const setView = useMapStore(state => state.setView);
    const setBboxFromMap = useFiltersStore(state => state.setBboxFromMap);

    const map = useMapEvents({
        moveend: () => {
            const c = map.getCenter();
            const z = map.getZoom();
            const bounds = map.getBounds();

            // 1. Vždy synchronizujeme URL/střed (pro MapStore)
            setView([c.lat, c.lng], z);

            // 2. Pokud je pohyb "programový", ignorujeme update filtrů a vypneme flag
            if (programmaticRef.current) {
                programmaticRef.current = false;
                return;
            }

            // 3. Jinak aktualizujeme BBox ve filtrech
            setBboxFromMap(
                bounds.getNorth(),
                bounds.getSouth(),
                bounds.getEast(),
                bounds.getWest()
            );
        },
    });

    // Inicializace BBoxu při prvním renderu mapy
    useEffect(() => {
        const bounds = map.getBounds();
        setBboxFromMap(
            bounds.getNorth(),
            bounds.getSouth(),
            bounds.getEast(),
            bounds.getWest()
        );
    }, []);

    return null;
};

const Map: React.FC<Props> = ({center, zoom, location, userLocation, loadingLocation, productUrl, programmaticRef}) => {
    const hoveredId = useFeaturesStore(state => state.hoveredFeatureId);
    const hoveredFeature = useFeaturesStore(state =>
        state.features.find(f => f.id === hoveredId)
    );

    return (
        <>
            <MapContainer center={center} zoom={zoom} className="w-100 h-100">
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution="&copy; OpenStreetMap contributors"
                />

                {/* Vykreslení polygonu při hoveru */}
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

                {userLocation && location && <UserLocationMarker location={location} />}
                {productUrl && <ProductLayer productUrl={productUrl} opacity={1} />}

                <MapUpdater programmaticRef={programmaticRef} />
            </MapContainer>
        </>
    );
};

export default Map;