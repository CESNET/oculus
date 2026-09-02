import {getVisualizationRequestPayload} from "../../utils/visualizationRequest.ts";
import type {VisualizationOptions, VisualizationResult, JobEventData} from "../../types/visualization.ts";
import type {Feature} from "../../types/feature.ts";

// ==========================================
// CONFIG
// ==========================================

// const API_URL = import.meta.env.VITE_API_URL || "/api";
const API_URL = "/api";

if (!API_URL) {
    throw new Error(
        "VITE_API_URL is not defined in environment variables"
    );
}

// ==========================================
// PUBLIC API
// ==========================================

export const requestVisualization = async (
    feature: Feature,
    options: VisualizationOptions = {}
): Promise<VisualizationResult> => {
    const job_id = await createVisualizationJob(
        feature,
        options.signal
    );

    return waitForJobCompletion(job_id, options);
};

// ==========================================
// JOB CREATION
// ==========================================

const createVisualizationJob = async (
    feature: Feature,
    signal?: AbortSignal
): Promise<string> => {
    const payload = getVisualizationRequestPayload(feature);

    const res = await fetch(`${API_URL}/jobs/create`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
        signal,
    });

    if (!res.ok) {
        throw new Error(
            `Failed to create visualization: ${res.statusText}`
        );
    }

    const data = await res.json();

    return data.job_id;
};

// ==========================================
// SSE WAIT
// ==========================================

const waitForJobCompletion = (
    job_id: string,
    {
        signal,
        onMessage,
        onCancel,
    }: VisualizationOptions = {}
): Promise<VisualizationResult> => {
    return new Promise((resolve, reject) => {
        const eventSource = new EventSource(
            `${API_URL}/jobs/${job_id}/events`
        );

        const cleanup = () => {
            eventSource.close();

            if (signal) {
                signal.removeEventListener(
                    "abort",
                    abortHandler
                );
            }
        };

        const abortHandler = async () => {
            cleanup();

            try {
                await cancelVisualizationJob(job_id);
            } catch (err) {
                console.error(
                    "Failed to send cancel request:",
                    err
                );
            }

            onCancel?.();

            reject(
                new DOMException(
                    "Aborted by user",
                    "AbortError"
                )
            );
        };

        if (signal) {
            if (signal.aborted) {
                abortHandler();
                return;
            }

            signal.addEventListener(
                "abort",
                abortHandler
            );
        }

        eventSource.onmessage = (event) => {
            try {
                const data: JobEventData = JSON.parse(
                    event.data
                );

                onMessage?.(data.current_status);

                switch (data.current_status) {
                    case "FINISHED":
                        cleanup();

                        resolve({
                            job_id: data.job_id,
                            visualizations:
                                data.visualizations ?? {},
                        });

                        break;

                    case "FAILED":
                    case "DOWNLOADING_FAILED":
                    case "PROCESSING_FAILED":
                    case "FINALIZING_FAILED":
                    case "CANCELLED":
                        cleanup();

                        reject(
                            new Error(
                                `Visualization job ended with status: ${data.current_status}`
                            )
                        );

                        break;
                }
            } catch (err) {
                console.error(
                    "Invalid SSE data received:",
                    event.data,
                    err
                );
            }
        };

        eventSource.onerror = () => {
            cleanup();

            reject(
                new Error(
                    "SSE connection error"
                )
            );
        };
    });
};

// ==========================================
// CANCEL
// ==========================================

export const cancelVisualizationJob = async (
    job_id: string
) => {
    try {
        await fetch(`${API_URL}/jobs/cancel`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({job_id}),
        });

        console.info(
            `Cancel request sent for job ${job_id}`
        );
    } catch (err) {
        console.error(
            `Failed to cancel job ${job_id}:`,
            err
        );
    }
};