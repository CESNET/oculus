import {useFiltersStore} from "./useFiltersStore";

export const useSentinel1Store = () => {
    const sentinel1 = useFiltersStore(state => state.sentinel1);

    const toggleLevel = (level: string) => {
        useFiltersStore.setState(state => {
            const levels = state.sentinel1.levels.includes(level)
                ? state.sentinel1.levels.filter(l => l !== level)
                : [...state.sentinel1.levels, level];

            return {sentinel1: {...state.sentinel1, levels}};
        });
    };

    const toggleSensingType = (type: string) => {
        useFiltersStore.setState(state => {
            const sensingTypes = state.sentinel1.sensingTypes.includes(type)
                ? state.sentinel1.sensingTypes.filter(t => t !== type)
                : [...state.sentinel1.sensingTypes, type];

            return {sentinel1: {...state.sentinel1, sensingTypes}};
        });
    };

    const toggleProductType = (type: string) => {
        useFiltersStore.setState(state => {
            const productTypes = state.sentinel1.productTypes.includes(type)
                ? state.sentinel1.productTypes.filter(t => t !== type)
                : [...state.sentinel1.productTypes, type];

            return {sentinel1: {...state.sentinel1, productTypes}};
        });
    };

    const togglePolarization = (pol: string) => {
        useFiltersStore.setState(state => {
            const polarizations = state.sentinel1.polarizations.includes(pol)
                ? state.sentinel1.polarizations.filter(p => p !== pol)
                : [...state.sentinel1.polarizations, pol];

            return {sentinel1: {...state.sentinel1, polarizations}};
        });
    };

    return {
        sentinel1,
        toggleLevel,
        toggleSensingType,
        toggleProductType,
        togglePolarization
    };
};