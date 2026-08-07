import type {Dataset} from "../datasets";
import type {VisualizationOutput} from "../visualization.ts";
import type {Sentinel2Visualizations} from "./sentinel2";

export interface VisualizationProperties {
    quality: number;
    zoom_levels: number[];
    outputs: Record<string, VisualizationOutput>;
    visualizations?: Sentinel2Visualizations;
}

export interface VisualizationRequest {
    dataset: Dataset;
    metadata?: Record<string, string>;
    properties: VisualizationProperties;
}