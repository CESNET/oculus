import React from 'react';
import {useMap} from 'react-leaflet';
import './Map.css';

interface Props {
    lat: number;
    lng: number;
    loading: boolean;
    zoom: number;
}

const LocateButton: React.FC<Props> = ({lat, lng, loading, zoom}) => {
    const map = useMap();

    const hasValidLocation =
        typeof lat === 'number' && typeof lng === 'number';

    const handleClick = () => {
        if (loading || !hasValidLocation) return;

        map.flyTo([lat, lng], zoom, {
            animate: true,
            duration: 1.2,
        });
    };

    return (
        <button
            type="button"
            onClick={handleClick}
            className={`btn btn-light map-locate-btn ${
                loading ? 'loading' : ''
            }`}
            title="Find my location"
        >
            {loading ? (
                <span className="spinner-border spinner-border-sm"/>
            ) : (
                <i className="bi bi-crosshair"/>
            )}
        </button>
    );
};

export default LocateButton;