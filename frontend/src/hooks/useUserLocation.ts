import { useState, useEffect } from 'react';

interface Location {
    lat: number;
    lng: number;
}

const DEFAULT_LOCATION: Location = { lat: 50.0755, lng: 14.4378 }; // Prague

export const useUserLocation = (): Location => {
    const [location, setLocation] = useState<Location>(DEFAULT_LOCATION);

    useEffect(() => {
        if (!navigator.geolocation) return;

        navigator.geolocation.getCurrentPosition(
            (pos) => {
                setLocation({ lat: pos.coords.latitude, lng: pos.coords.longitude });
            },
            (err) => {
                console.warn('Geolocation denied or failed, using default', err);
            },
            { enableHighAccuracy: true }
        );
    }, []);

    return location;
};