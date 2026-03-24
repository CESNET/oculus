import React from 'react';
import {MapContainer, TileLayer} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

import {useUserLocation, DEFAULT_LOCATION} from '../../hooks/useUserLocation';
import LocateButton from './LocateButton';
import UserLocationMarker from './UserLocationMarker';
import ProductLayer from './layers/ProductLayer';

import './Map.css';

interface Props {
    zoom?: number;
    productUrl?: string; // URL for the selected product overlay
}

const Map: React.FC<Props> = ({zoom = 13, productUrl}) => {
    const {location, loading, error} = useUserLocation();

    return (
        <div className="map-wrapper">
            <MapContainer
                center={[DEFAULT_LOCATION.lat, DEFAULT_LOCATION.lng]}
                zoom={zoom}
                className="w-100 h-100"
            >
                {/* Base map */}
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution="&copy; OpenStreetMap contributors"
                />

                {/* User location marker and accuracy */}
                <UserLocationMarker location={location}/>

                {/* Product overlay (conditionally rendered) */}
                {productUrl && <ProductLayer productUrl={productUrl} opacity={1}/>}

                {/* Locate button */}
                <LocateButton
                    lat={location.lat}
                    lng={location.lng}
                    loading={loading}
                    zoom={zoom}
                />
            </MapContainer>

            {/* Error message */}
            {error && (
                <div className="map-error alert alert-light py-1 px-2">
                    {error}
                </div>
            )}
        </div>
    );
};

export default Map;