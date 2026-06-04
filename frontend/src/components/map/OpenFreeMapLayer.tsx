import {useEffect} from 'react';
import {useMap} from 'react-leaflet';

import 'maplibre-gl';
import '@maplibre/maplibre-gl-leaflet';

const OpenFreeMapLayer = () => {
    const map = useMap();

    useEffect(() => {
        // @ts-ignore
        const layer = L.maplibreGL({
            style: 'https://tiles.openfreemap.org/styles/liberty'
        });

        layer.addTo(map);

        return () => {
            map.removeLayer(layer);
        };
    }, [map]);

    return null;
};

export default OpenFreeMapLayer;
