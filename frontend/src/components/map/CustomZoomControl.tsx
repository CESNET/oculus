import { useEffect, useRef } from "react";
import { useMap } from "react-leaflet";
import L from "leaflet";

export default function CustomZoomControl() {
    const map = useMap();
    const controlRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const element = controlRef.current;
        if (!element) return;

        L.DomEvent.disableClickPropagation(element);
        L.DomEvent.disableScrollPropagation(element);

        return () => {
            L.DomEvent.off(element);
        };
    }, []);

    return (
        <div
            ref={controlRef}
            className="map-zoom-control"
            role="group"
            aria-label="Map zoom controls"
        >
            <button
                type="button"
                onClick={() => map.zoomOut()}
                aria-label="Zoom out"
                title="Zoom out"
            >
                <i className="bi bi-dash" aria-hidden="true" />
            </button>

            <button
                type="button"
                onClick={() => map.zoomIn()}
                aria-label="Zoom in"
                title="Zoom in"
            >
                <i className="bi bi-plus" aria-hidden="true" />
            </button>
        </div>
    );
}
