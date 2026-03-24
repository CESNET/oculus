import React from 'react';
import {Marker, Circle} from 'react-leaflet';
import L from 'leaflet';
import './Map.css';

interface Location {
    lat: number;
    lng: number;
    accuracy?: number;
}

interface Props {
    location: Location;
}

/* Custom user location dot */
const userLocationIcon = L.divIcon({
    className: 'user-location-marker',
    html: '<div class="dot"></div>',
    iconSize: [20, 20],
    iconAnchor: [10, 10],
});

const UserLocationMarker: React.FC<Props> = ({location}) => {
    const hasLocation =
        typeof location?.lat === 'number' &&
        typeof location?.lng === 'number';

    const accuracy =
        location.accuracy && location.accuracy > 0
            ? Math.min(location.accuracy, 300)
            : 0;

    if (!hasLocation) return null;

    return (
        <>
            <Marker
                position={[location.lat, location.lng]}
                icon={userLocationIcon}
            />
            {accuracy > 0 && (
                <Circle
                    center={[location.lat, location.lng]}
                    radius={accuracy}
                    className="accuracy-circle"
                    pathOptions={{opacity: 0}}
                />
            )}
        </>
    );
};

export default UserLocationMarker;
