import React from "react";
import {useMap} from "react-leaflet";

interface Props {
    zoom: number;
    loading: boolean;
    programmaticRef: React.MutableRefObject<boolean>;
}

const LocateButton: React.FC<Props> = (
    {
        loading,
        zoom,
        programmaticRef,
    }
) => {
    const map = useMap();
    const [locating, setLocating] = React.useState(false);
    const [error, setError] = React.useState<string | null>(null);

    const handleClick = () => {
        if (loading || locating) return;

        if (!navigator.geolocation) {
            setError("Geolocation is not supported by your browser.");
            return;
        }

        setLocating(true);
        setError(null);

        navigator.geolocation.getCurrentPosition(
            (position) => {
                programmaticRef.current = false;

                map.flyTo(
                    [
                        position.coords.latitude,
                        position.coords.longitude,
                    ],
                    zoom,
                    {
                        animate: true,
                        duration: 1.0,
                    },
                );

                setLocating(false);
            },
            (geolocationError) => {

                switch (geolocationError.code) {
                    case geolocationError.PERMISSION_DENIED:
                        setError(
                            "Location access denied. Please allow location access in your browser settings and try again."
                        );
                        break;

                    case geolocationError.POSITION_UNAVAILABLE:
                        setError(
                            "Your location is currently unavailable. Please try again."
                        );
                        break;

                    case geolocationError.TIMEOUT:
                        setError(
                            "Location request timed out. Please try again."
                        );
                        break;

                    default:
                        setError(
                            "Unable to determine your location. Please try again."
                        );
                }

                setLocating(false);
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0,
            },
        );
    };

    const disabled = loading || locating;

    return (
        <>
            <button
                type="button"
                onClick={handleClick}
                disabled={disabled}
                className={`map-locate-btn ${disabled ? "disabled" : ""}`}
                title="Find my location"
                aria-label="Find my location"
            >
                {locating || loading ? (
                    <span className="spinner-border spinner-border-sm" />
                ) : (
                    <i className="bi bi-crosshair" />
                )}
            </button>


            {error && (
                <div
                    className="alert alert-warning alert-dismissible fade show map-locate-error"
                    role="alert"
                >
                    <i className="bi bi-exclamation-triangle-fill me-2" />
                    {error}

                    <button
                        type="button"
                        className="btn-close"
                        aria-label="Close"
                        onClick={() => setError(null)}
                    />
                </div>
            )}

        </>
    );
};

export default LocateButton;
