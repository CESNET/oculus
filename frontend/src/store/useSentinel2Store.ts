import { useFiltersStore } from "./useFiltersStore";

export const useSentinel2Store = () => {
    const sentinel2 = useFiltersStore(state => state.sentinel2);

    // toggle pro pole levels
    const toggleLevel = (level: string) => {
        useFiltersStore.setState(state => {
            const levels = state.sentinel2.levels.includes(level)
                ? state.sentinel2.levels.filter(l => l !== level)
                : [...state.sentinel2.levels, level];
            return { sentinel2: { ...state.sentinel2, levels } };
        });
    };

    // toggle pro bands
    const toggleBand = (band: string) => {
        useFiltersStore.setState(state => {
            const bands = state.sentinel2.bands.includes(band)
                ? state.sentinel2.bands.filter(b => b !== band)
                : [...state.sentinel2.bands, band];
            return { sentinel2: { ...state.sentinel2, bands } };
        });
    };

    const setCloudCover = (cloudCover: number) => {
        useFiltersStore.setState(state => ({ sentinel2: { ...state.sentinel2, cloudCover } }));
    };

    return { sentinel2, toggleLevel, toggleBand, setCloudCover };
};