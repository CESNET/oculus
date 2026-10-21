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


// ======================================================
// REQUEST
// ======================================================

/**
 * Output configuration sent to the backend.
 */
export interface VisualizationRequestOutput {
    full_product: boolean;
    wm_tiles: boolean;
}


// ======================================================
// RESPONSE
// ======================================================

/**
 * Actual output generated for one format.
 */
export interface VisualizationFormatOutput {
    full_product: string | null;
    wm_tiles: string | null;
    wm_tiles_zoom_levels: number[];
}


/**
 * Actual visualization result.
 *
 * Key in the parent `visualizations` object is the
 * visualization ID, e.g. "TCI", "B02",
 * "rgb_B04-B8A-B11", "ndvi_B08-B04".
 */
export interface ProcessedFileState {
    outputs: Partial<
        Record<OutputFormat, VisualizationFormatOutput>
    >;
}


// ======================================================
// NORMALIZED OUTPUTS
// ======================================================

export interface ProductFile {
    path: string;
    name: string;
    format: OutputFormat;
}

export interface TileLayer {
    path: string;
    name: string;
    format: OutputFormat;
    zoomLevels: number[];
}


// ======================================================
// API RESPONSE
// ======================================================

export interface VisualizationResult {
    job_id: string;
    visualizations: Record<string, ProcessedFileState>;
}


export interface JobEventData {
    job_id: string;
    current_status: JobStatus;

    visualizations?: Record<string, ProcessedFileState>;
}


// ======================================================
// REQUEST OPTIONS
// ======================================================

export interface VisualizationOptions {
    signal?: AbortSignal;
    onMessage?: (status: JobStatus) => void;
    onCancel?: () => void;
}
