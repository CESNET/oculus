import React, { useState } from "react";
import Map from "../components/map/Map";

export default function MapLayout() {
    // Placeholder for dynamic overlay URL (or any other overlay data)
    const [overlayUrl, setOverlayUrl] = useState<string | undefined>();

    // Example: overlay will be controlled by another component in the future
    // You can pass overlayUrl to Map as a prop when ready
    // <Map overlayUrl={overlayUrl} />

    return (
        <div style={{ height: "100vh", width: "100%" }}>
            {/* Map component */}
            <Map
                // Currently no overlay; overlayUrl prop can be added later
                // overlayUrl={overlayUrl}
            />
        </div>
    );
}