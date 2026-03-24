import React from 'react';
import { TileLayer } from 'react-leaflet';

interface Props {
    productUrl: string;   // root URL of the selected product
    opacity?: number;     // layer opacity (0–1), can come from a slider
}

const ProductLayer: React.FC<Props> = ({ productUrl, opacity = 1 }) => {
    if (!productUrl) return null; // don't render if no product

    return (
        <TileLayer
            url={`${productUrl}/{z}/{x}/{y}.png`}
            opacity={opacity}
            attribution="Remote Sensing Data"
        />
    );
};

export default ProductLayer;