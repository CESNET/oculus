import {requestVisualization} from "../api/backend/requestVisualization";

import {useVisualizationStore} from "../store/useVisualizationStore";
import {useLoadingStore} from "../store/useLoadingStore";
import {useSidebarStore} from "../store/useSidebarStore";


import type {Feature} from "../types/feature.ts";
import {applyVisualizationResults} from "../utils/visualizationUtils.ts";

export async function runVisualization(feature: Feature) {
    const {startLoading, stopLoading} = useLoadingStore.getState();

    const controller = startLoading();

    try {
        const visualizationStore =
            useVisualizationStore.getState();

        const {job_id, processed_files} =
            await requestVisualization(feature, {
                signal: controller.signal,
                onMessage: (status) =>
                    console.log("Job status:", status),
            });

        visualizationStore.setJobId(job_id);
        visualizationStore.setFeatureId(feature.id);

        applyVisualizationResults(processed_files);

        if (useSidebarStore.getState().activeTab !== 2) {
            useSidebarStore.getState().setActiveTab(2);
        }

    } catch (err: any) {
        if (err.name === "AbortError") {
            console.log("Visualization aborted");
        } else {
            console.error("Error during visualization:", err);
        }
    } finally {
        stopLoading();
    }
}
