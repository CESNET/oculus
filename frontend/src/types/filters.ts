export interface BoundingBox {
    north: number;
    south: number;
    east: number;
    west: number;
}

export interface DatetimeRange {
    start: string;
    end: string;
}

export interface Sentinel1Filter {
    levels: string[];
    operationalModes: string[];
    productTypes: string[];
    polarizations: string[];
}

export interface Sentinel2Filter {
    cloudCover: number | null;
    levels: string[];
}