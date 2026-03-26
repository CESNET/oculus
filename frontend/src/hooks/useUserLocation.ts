import {useState, useEffect} from 'react';

export interface Location {
    lat: number;
    lng: number;
    accuracy?: number;
}

export const DEFAULT_LOCATION: Location = {
    lat: 50.0755,
    lng: 14.4378,
};

export const useUserLocation = () => {
    const isSupported =
        typeof navigator !== 'undefined' &&
        'geolocation' in navigator;

    const [location, setLocation] = useState<Location>(DEFAULT_LOCATION);
    const [loading, setLoading] = useState(isSupported);
    const [isUserLocation, setIsUserLocation] = useState(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(
        isSupported ? null : 'Geolocation is not supported'
    );

    useEffect(() => {
        if (!isSupported) return;

        navigator.geolocation.getCurrentPosition(
            (position) => {
                setLocation({
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                    accuracy: position.coords.accuracy,
                });
                setIsUserLocation(true);
                setLoading(false);
            },
            (error) => {
                console.error('Failed to get location:', error);
                setIsUserLocation(false);
                setErrorMessage('Using default location');
                setLoading(false);
            },
            { enableHighAccuracy: true, timeout: 20000 }
        );
    }, [isSupported]);

    console.log(location, loading, isUserLocation, errorMessage);
    return {
        location: location,
        loading: loading,
        isUserLocation: isUserLocation,
        errorMessage: errorMessage
    };
};
