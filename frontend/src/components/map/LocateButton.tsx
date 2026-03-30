import React from 'react';
import { useMap } from 'react-leaflet';

interface Props {
    lat: number;
    lng: number;
    zoom: number;
    loading: boolean;
    userLocation: boolean;
    programmaticRef: React.MutableRefObject<boolean>;
}

const LocateButton: React.FC<Props> = ({ lat, lng, loading, zoom, userLocation, programmaticRef }) => {
    const map = useMap();
    const isEnabled = !loading && userLocation;

    const handleClick = () => {
        if (!isEnabled) return;

        programmaticRef.current = false;

        map.flyTo([lat, lng], zoom, {
            animate: true,
            duration: 1.0,
        });
    };

    return (
        <button
            type="button"
            onClick={handleClick}
            className={`btn btn-light map-locate-btn ${!isEnabled ? 'disabled' : ''}`}
        >
            {loading ? <span className="spinner-border spinner-border-sm" /> : <i className="bi bi-crosshair" />}
        </button>
    );
};

export default LocateButton;