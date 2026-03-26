import React from 'react';
import {MapContainer, TileLayer, useMapEvents} from 'react-leaflet';
import {useMapStore} from '../../store/mapStore';
import UserLocationMarker from './UserLocationMarker';
import LocateButton from './LocateButton';
import ProductLayer from './layers/ProductLayer';
import type {LatLngExpression} from 'leaflet';
import {toLatLngTuple} from '../../utils/map';

interface Props {
    center: LatLngExpression;
    zoom: number;
    location?: { lat: number; lng: number };
    userLocation?: boolean;
    loadingLocation?: boolean;
    productUrl?: string;
}

const Map: React.FC<Props> = ({
                                  center,
                                  zoom,
                                  location,
                                  userLocation,
                                  loadingLocation,
                                  productUrl
                              }) => {
    const setView = useMapStore(state => state.setView);

    const MapUpdater = () => {
        useMapEvents({
            moveend: (e) => {
                const map = e.target;
                const c = map.getCenter();
                setView([c.lat, c.lng], map.getZoom());
            },
            zoomend: (e) => {
                const map = e.target;
                const c = map.getCenter();
                setView([c.lat, c.lng], map.getZoom());
            },
        });
        return null;
    };

    const [lat, lng] = toLatLngTuple(center);

    return (
        <MapContainer center={center} zoom={zoom} className="w-100 h-100">
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="&copy; OpenStreetMap contributors"
            />

            {/* Locate button enabled jen pokud známe userLocation */}
            <LocateButton
                lat={location?.lat ?? lat}
                lng={location?.lng ?? lng}
                userLocation={!!userLocation} // enabled pouze pokud máme skutečnou polohu
                loading={loadingLocation ?? false}
                zoom={zoom}
            />

            {/* Marker jen pokud máme skutečnou polohu uživatele */}
            {userLocation && location && <UserLocationMarker location={location} />}

            {/* Product overlay */}
            {productUrl && <ProductLayer productUrl={productUrl} opacity={1} />}

            <MapUpdater />
        </MapContainer>
    );
};

export default Map;