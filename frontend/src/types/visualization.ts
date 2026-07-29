export type JobStatus =
    | "ACCEPTED"
    | "DOWNLOADING"
    | "DOWNLOADING_COMPLETE"
    | "DOWNLOADING_FAILED"
    | "PROCESSING"
    | "PROCESSING_COMPLETE"
    | "PROCESSING_FAILED"
    | "FINALIZING"
    | "FINALIZING_FAILED"
    | "FINISHED"
    | "FAILED"
    | "CANCELLED";

export interface ProcessedFileState {
    filename: string;
    download_path: string;

    full_product: {
        jpg: string | null;
        png: string | null;
        webp: string | null;
    };

    wm_tiles: {
        jpg: string | null;
        png: string | null;
        webp: string | null;
    };

    wm_tiles_zoom_levels: number[];
}

export interface VisualizationOutput {
    full_product: boolean;
    wm_tiles: boolean;
}

export interface ProductFile {
    path: string;
    name: string; // with extension
    format: string;
}


export interface TileLayer {
    path: string; // path to folder with tiles
    name: string; // without extension
    format: string; // webp, jpg, png
    zoomLevels: number[];
}

export interface VisualizationResult {
    job_id: string;
    processed_files: Record<string, ProcessedFileState>;
}

export interface JobEventData {
    job_id: string;
    current_status: JobStatus;

    processed_files?: Record<string, ProcessedFileState>;
}

export interface VisualizationOptions {
    signal?: AbortSignal;
    onMessage?: (msg: JobStatus) => void;
    onCancel?: () => void;
}