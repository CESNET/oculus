export const Dataset = {
    Sentinel1: "Sentinel-1",
    Sentinel2: "Sentinel-2",
    Landsat: "Landsat",
} as const;

export type Dataset = (typeof Dataset)[keyof typeof Dataset];
