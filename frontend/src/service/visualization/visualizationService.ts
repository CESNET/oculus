import {requestVisualization} from "../../api/backend/requestVisualization";

import {useVisualizationStore} from "../../store/useVisualizationStore";
import {useLoadingStore} from "../../store/useLoadingStore";
import {useSidebarStore} from "../../store/useSidebarStore";

import type {Feature} from "../../types/feature.ts";
import {applyVisualizationResults} from "../../utils/visualizationUtils.ts";

import {initializeSentinel1Visualization} from "./sentinel1VisualizationService.ts";
import {Dataset} from "../../types/datasets.ts";


export const runVisualization = async (feature: Feature) => {
    const {startLoading, stopLoading} = useLoadingStore.getState();

    const controller = startLoading();

    try {
        const visualizationStore = useVisualizationStore.getState();

        if (feature.dataset === Dataset.Sentinel1) {
            initializeSentinel1Visualization(feature);
        }

        const {job_id, visualizations} = await requestVisualization(feature, {
            signal: controller.signal,
            onMessage: (status) =>
                console.log("Job status:", status),
        });

        visualizationStore.setJobId(job_id);
        visualizationStore.setFeatureId(feature.id);

        applyVisualizationResults(visualizations);

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
};