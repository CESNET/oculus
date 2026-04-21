import React, {useEffect} from 'react';
import {
    MapContainer,
    TileLayer,
    useMapEvents,
    useMap,
    Polygon
} from 'react-leaflet';

import type {LatLngExpression} from 'leaflet';

import {polygonToBounds, registerMap} from '../../utils/mapUtils';
import {useMapStore} from '../../store/useMapStore';
import {useFiltersStore} from '../../store/useFiltersStore';
import {useFeaturesStore} from '../../store/useFeaturesStore';
import {useVisualizationStore} from '../../store/useVisualizationStore';

import UserLocationMarker from './UserLocationMarker';
import LocateButton from './LocateButton';
import ProductLayer from './layers/ProductLayer';

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
const MapUpdater = ({programmaticRef}: any) => {
    const setView = useMapStore((s) => s.setView);
    const setBboxFromMap = useFiltersStore((s) => s.setBboxFromMap);

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

    // =============================
    // FEATURES
    // =============================
    const hoveredFeatureId = useFeaturesStore((s) => s.hoveredFeatureId);

    const hoveredFeature = useFeaturesStore((s) =>
        hoveredFeatureId ? s.featuresById[hoveredFeatureId] : undefined
    );

    // =============================
    // VISUALIZATION
    // =============================
    const {
        tileLayers,
        selectedTileLayerIndex,
        availableZoomLevels,
        opacity,
        featureId
    } = useVisualizationStore();

    const feature = useFeaturesStore((s) =>
        featureId ? s.featuresById[featureId] : undefined
    );

    const selectedTile =
        selectedTileLayerIndex !== null
            ? tileLayers[selectedTileLayerIndex]
            : null;

    const featureBounds = feature
        ? polygonToBounds(feature.geometry.coordinates)
        : undefined;

    // =============================
    // RENDER
    // =============================
    return (
        <MapContainer center={center} zoom={zoom} className="w-100 h-100">

            {/* Base map */}
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="&copy; OpenStreetMap contributors"
            />

            {/* Hover highlight */}
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

            {/* User location controls */}
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

            {/* Product layer */}
            {productUrl && (
                <ProductLayer productUrl={productUrl} opacity={1} />
            )}

            {/* Visualization tile layer */}
            {selectedTile && (
                <TileLayer
                    url={`${selectedTile.path}/{z}/{x}/{y}.${selectedTile.format}`}
                    opacity={opacity}
                    maxNativeZoom={availableZoomLevels.at(-1)}
                    minNativeZoom={availableZoomLevels.at(0)}
                    bounds={featureBounds}
                />
            )}

            <MapRegistrar />
            <MapUpdater programmaticRef={programmaticRef} />
        </MapContainer>
    );
};

export default Map;