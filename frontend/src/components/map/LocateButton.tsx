import React from 'react';
import { useMap } from 'react-leaflet';
import './Map.css';

interface Props {
    lat: number;
    lng: number;
    zoom: number;
    loading: boolean;
    userLocation: boolean; // true pouze pokud máme skutečnou polohu
}

const LocateButton: React.FC<Props> = ({ lat, lng, loading, zoom, userLocation }) => {
    const map = useMap();

    const isEnabled = !loading && userLocation;

    const handleClick = () => {
        if (!isEnabled) return;

        map.flyTo([lat, lng], zoom, {
            animate: true,
            duration: 1.2,
        });
    };

    //if (!userLocation) return null;

    return (
        <button
            type="button"
            onClick={() => {
                if (!isEnabled) {
                    console.warn('User location unavailable'); // todo vypsat nějaký alert
                    return;
                }
                handleClick();
            }}
            className={`btn btn-light map-locate-btn ${!isEnabled ? 'not-available' : ''}`}
            title={isEnabled ? "Find my location" : "Location unavailable"}
        >
            {loading ? (
                <span className="spinner-border spinner-border-sm" />
            ) : (
                <i className="bi bi-crosshair" />
            )}
        </button>
    );
};

export default LocateButton;