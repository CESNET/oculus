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


export type OutputFormat = "jpg" | "png" | "webp";


export interface VisualizationFormatOutput {
    full_product: string | null;
    wm_tiles: string | null;
    wm_tiles_zoom_levels: number[];
}


export interface ProcessedFileState {
    outputs: Partial<Record<OutputFormat, VisualizationFormatOutput>>;
}


export interface VisualizationResult {
    job_id: string;
    visualizations: Record<string, ProcessedFileState>;
}


export interface JobEventData {
    job_id: string;
    current_status: JobStatus;
    visualizations?: Record<string, ProcessedFileState>;
}


export interface ProductFile {
    path: string;
    name: string; // with extension
    format: OutputFormat;
}


export interface TileLayer {
    path: string; // path to folder with tiles
    name: string; // without extension
    format: OutputFormat;
    zoomLevels: number[];
}


export interface VisualizationOptions {
    signal?: AbortSignal;
    onMessage?: (msg: JobStatus) => void;
    onCancel?: () => void;
}