import {useState, useEffect} from 'react';

interface Location {
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
    const [error, setError] = useState<string | null>(
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
                setLoading(false);
            },
            () => {
                setError('Using default location');
                setLoading(false);
            }
        );
    }, [isSupported]);

    return {location, loading, error};
};
