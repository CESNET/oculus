import React from 'react';
import {MapContainer, TileLayer, Marker, Popup} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import {useUserLocation} from '../../hooks/useUserLocation';

interface Props {
    onOpenSidebar: () => void;
}

const MapContainerWrapper: React.FC<Props> = ({onOpenSidebar}) => {
    const userLocation = useUserLocation();

    return (
        <div className="flex-fill position-relative" style={{height: '100%'}}>
            {/* Leaflet map */}
            <MapContainer
                center={[userLocation.lat, userLocation.lng]}
                zoom={13}
                style={{height: '100%', width: '100%'}}
            >
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution="&copy; OpenStreetMap contributors"
                />
                <Marker position={[userLocation.lat, userLocation.lng]}>
                    <Popup>User (or default) location</Popup>
                </Marker>
            </MapContainer>
        </div>
    );
};

export default MapContainerWrapper;