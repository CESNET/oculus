import {type Feature} from "../../store/useFeaturesStore.ts";
import {visualizeFeature} from "../../utils/featureUtils.ts";

export interface VisualizationOptions {
    /** Optional AbortSignal to cancel the request (user action only) */
    signal?: AbortSignal;
    /** Callback for real-time job status updates */
    onMessage?: (msg: JobStatus) => void;
    /** Callback to trigger user-initiated cancel */
    onCancel?: () => void;
}

/**
 * Load API URL from environment variables
 */
// const API_URL = import.meta.env.VITE_API_URL || "/api"; // TODO some problem with variable import
const API_URL: string = "/api";

if (!API_URL) {
    throw new Error("VITE_API_URL is not defined in environment variables");
}

/**
 * All possible job statuses from the backend
 */
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

interface JobEventData {
    job_id: string;
    status: JobStatus;
    processed_files?: string[];
}

/**
 * Main function to request visualization for a feature.
 * Handles job creation and waits for completion using SSE.
 */
export const requestVisualization = async (
    feature: Feature,
    options: VisualizationOptions = {}
) => {
    const job_id = await createVisualizationJob(feature, options.signal);
    return waitForJobCompletion(job_id, options);
};

const createVisualizationJob = async (feature: Feature, signal?: AbortSignal): Promise<string> => {
    const payload = visualizeFeature(feature);

    const res = await fetch(`${API_URL}/jobs/create`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload),
        signal,
    });

    if (!res.ok) {
        throw new Error(`Failed to create visualization: ${res.statusText}`);
    }

    const data = await res.json();
    return data.job_id;
};

const waitForJobCompletion = (
    job_id: string,
    {signal, onMessage, onCancel}: VisualizationOptions = {}
): Promise<{ job_id: string; processed_files: string[] }> => {
    return new Promise((resolve, reject) => {
        const eventSource = new EventSource(`${API_URL}/jobs/${job_id}/events`);

        const cleanup = () => eventSource.close();

        // User-initiated cancel
        if (signal) {
            signal.addEventListener("abort", () => {
                cleanup();
                if (onCancel) onCancel();
                reject(new DOMException("Aborted by user", "AbortError"));
            });
        }

        eventSource.onmessage = (event) => {
            try {
                const data: JobEventData = JSON.parse(event.data);
                if (onMessage) onMessage(data.status);

                switch (data.status) {
                    case "FINISHED":
                        cleanup();
                        resolve({
                            job_id: data.job_id,
                            processed_files: data.processed_files || [],
                        });
                        break;
                    case "FAILED":
                    case "DOWNLOADING_FAILED":
                    case "PROCESSING_FAILED":
                    case "FINALIZING_FAILED":
                    case "CANCELLED":
                        cleanup();
                        reject(new Error(`Visualization job ended with status: ${data.status}`));
                        break;
                    // other statuses: ACCEPTED, DOWNLOADING, PROCESSING, FINALIZING...
                }
            } catch (err) {
                console.error("Invalid SSE data received:", event.data, err);
            }
        };

        eventSource.onerror = (_err) => {
            cleanup();
            reject(new Error("SSE connection error"));
        };
    });
};

// Cancel only when user explicitly requests it
export const cancelVisualizationJob = async (job_id: string) => {
    try {
        await fetch(`${API_URL}/jobs/cancel`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({job_id}),
        });
        console.info(`Cancel request sent for job ${job_id}`);
    } catch (err) {
        console.error(`Failed to cancel job ${job_id}:`, err);
    }
};
