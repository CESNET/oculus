import {useEffect, useRef} from "react";
import L from "leaflet";

import CustomZoomControl from "./CustomZoomControl";
import LocateButton from "./LocateButton";

interface Props {
    lat: number;
    lng: number;
    zoom: number;
    loading: boolean;
    userLocation: boolean;
    programmaticRef: React.MutableRefObject<boolean>;
}

export default function MapTopControls(props: Props) {
    const controlsRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const element = controlsRef.current;
        if (!element) return;

        L.DomEvent.disableClickPropagation(element);
        L.DomEvent.disableScrollPropagation(element);

        return () => {
            L.DomEvent.off(element);
        };
    }, []);

    return (
        <div ref={controlsRef} className="map-top-controls">
            <LocateButton
                loading={props.loading}
                zoom={props.zoom}
                programmaticRef={props.programmaticRef}
            />

            <CustomZoomControl />
        </div>
    );
}
