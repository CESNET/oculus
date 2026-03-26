import { useEffect, useLayoutEffect, useState } from "react";
import Map from "../components/map/Map";
import { useMapStore } from "../store/mapStore";
import { useUserLocation, DEFAULT_LOCATION } from "../hooks/useUserLocation";
import { toLatLngTuple } from "../utils/map.ts";

export default function MapLayout() {
    const { center, zoom, setView } = useMapStore();
    const { location, loading, isUserLocation, errorMessage: locationErrorMessage } = useUserLocation();
    const [initialized, setInitialized] = useState(false);

    // -----------------------------
    // 1️⃣ Inicializace mapy podle URL nebo lokace uživatele
    // -----------------------------
    useLayoutEffect(() => {
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

        queueMicrotask(() => setInitialized(true));
    }, [location, setView]);

    // -----------------------------
    // 2️⃣ Synchronizace URL podle aktuálního stavu mapy
    // -----------------------------
    useEffect(() => {
        if (!initialized) return;

        const params = new URLSearchParams();
        const [lat, lng] = toLatLngTuple(center);

        params.set("lat", String(lat));
        params.set("lng", String(lng));
        params.set("zoom", String(zoom));

        window.history.replaceState(
            null,
            "",
            `${window.location.pathname}?${params.toString()}`
        );
    }, [center, zoom, initialized]);

    // -----------------------------
    // 3️⃣ Render
    // -----------------------------
    if (!initialized) return null;

    return (
        <div className="map-wrapper">
            <Map
                center={center}
                zoom={zoom}
                location={location}
                userLocation={isUserLocation}
                loadingLocation={loading}
            />
            {/*!isUserLocation && locationErrorMessage && (
                <div className="map-error">{locationErrorMessage}</div>
            )*/}
        </div>
    );
}