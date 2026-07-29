import type {Dataset} from "./datasets.ts";

export interface Feature {
    id: string;

    title: string;
    name: string;

    dataset: Dataset;

    platform: string;
    satellite?: string;
    productType?: string;

    acquisitionDateTime: string;

    productUrl: string;

    geometry: {
        type: "Polygon";
        coordinates: [number, number][][];
    };
}