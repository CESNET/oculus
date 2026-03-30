import { useEffect, useState, useRef } from "react";
import Map from "../components/map/Map";
import { useMapStore } from "../store/useMapStore";
import { useUserLocation, DEFAULT_LOCATION } from "../hooks/useUserLocation";
import { toLatLngTuple } from "../utils/map";

export default function MapLayout() {
    const { center, zoom, setView } = useMapStore();
    const { location, loading, isUserLocation } = useUserLocation();
    const [initialized, setInitialized] = useState(false);

    // Tento ref sdílíme s komponentou Map
    const programmaticRef = useRef(false);

    // 1. Načtení z URL při prvním startu
    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const lat = parseFloat(params.get("lat") || "");
        const lng = parseFloat(params.get("lng") || "");
        const z = parseInt(params.get("zoom") || "", 10);

        if (!isNaN(lat) && !isNaN(lng) && !isNaN(z)) {
            setView([lat, lng], z);
        } else if (location) {
            setView([location.lat, location.lng], 13);
        } else {
            setView([DEFAULT_LOCATION.lat, DEFAULT_LOCATION.lng], 13);
        }

        setInitialized(true);
    }, [location, setView]);

    // 2. Synchronizace URL (při změně center/zoom v MapStore)
    useEffect(() => {
        if (!initialized) return;

        const [lat, lng] = toLatLngTuple(center);
        const params = new URLSearchParams();
        params.set("lat", lat.toFixed(6));
        params.set("lng", lng.toFixed(6));
        params.set("zoom", zoom.toString());

        window.history.replaceState(null, "", `${window.location.pathname}?${params.toString()}`);
    }, [center, zoom, initialized]);

    if (!initialized) return null;

    return (
        <div className="map-wrapper" style={{ width: '100%', height: '100vh' }}>
            <Map
                center={center}
                zoom={zoom}
                location={location}
                userLocation={isUserLocation}
                loadingLocation={loading}
                programmaticRef={programmaticRef}
            />
        </div>
    );
}