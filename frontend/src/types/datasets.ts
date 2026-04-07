export const Dataset = {
    Sentinel1: "Sentinel-1",
    Sentinel2: "Sentinel-2",
    Landsat: "Landsat",
} as const;

export type Dataset = (typeof Dataset)[keyof typeof Dataset];


export const DatasetFamily = {
    Sentinel: "sentinel",
    Landsat: "landsat",
} as const;

export type DatasetFamily = (typeof DatasetFamily)[keyof typeof DatasetFamily];


export const DatasetToFamily: Record<Dataset, DatasetFamily> = {
    [Dataset.Sentinel1]: DatasetFamily.Sentinel,
    [Dataset.Sentinel2]: DatasetFamily.Sentinel,
    [Dataset.Landsat]: DatasetFamily.Landsat,
};
