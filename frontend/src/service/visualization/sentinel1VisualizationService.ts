import type {Feature} from "../../types/feature.ts";

import {useVisualizationStore} from "../../store/useVisualizationStore.ts";
import {getSentinel1Polarizations} from "../../api/datasources/helpers/sentinel1.ts";


export const initializeSentinel1Visualization = (
    feature: Feature,
): void => {
    const availablePolarizations = getSentinel1Polarizations(feature.name);

    useVisualizationStore.getState().setSentinel1({
        availablePolarizations: availablePolarizations,
        selectedPolarizations: availablePolarizations,
    });
};