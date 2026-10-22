export const LoadingType = {
    DEFAULT: "default",
    FETCH_FEATURES: "fetch-features",
    VISUALIZING: "visualizing",
    DOWNLOADING: "downloading",
    PROCESSING: "processing",
} as const;

export type LoadingType = (typeof LoadingType)[keyof typeof LoadingType];
