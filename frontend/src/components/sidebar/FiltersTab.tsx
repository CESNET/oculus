import { useFiltersStore } from "../../store/useFiltersStore";
import BoundingBoxFilter from "./filters/BoundingBoxFilter";
import DatetimeFilter from "./filters/DatetimeFilter";
import DatasetFilter from "./filters/DatasetFilter";
import { fetchFeatures } from "../../api/fetchFeatures";
import { useFeaturesStore } from "../../store/useFeaturesStore";
import { useLoadingStore } from "../../store/useLoadingStore";
import { getEffectiveFilters } from "../../utils/filterUtils.ts";

interface FiltersTabProps {
    onFetched?: () => void;
}

export default function FiltersTab({ onFetched }: FiltersTabProps) {
    const filters = useFiltersStore();
    const setFeatures = useFeaturesStore((state) => state.setFeatures);

    // Globální loading akce
    const startLoading = useLoadingStore((state) => state.startLoading);
    //const stopLoading = useLoadingStore((state) => state.stopLoading);
    const isLoading = useLoadingStore((state) => state.isLoading);

    const handleFetchFeatures = async () => {
        // 1. Spustíme loading a získáme nový AbortController
        const controller = startLoading();

        const effectiveFilters = getEffectiveFilters(filters, filters.dataset);

        // Synchronizace filtrů v store (volitelné, dle tvé logiky)
        useFiltersStore.getState().setFilters({
            sentinel1: effectiveFilters.sentinel1,
            sentinel2: effectiveFilters.sentinel2,
        });

        try {
            // 2. Předáme signal z controlleru do API volání
            const fetched = await fetchFeatures(
                effectiveFilters,
                filters.dataset,
                controller.signal
            );

            setFeatures(fetched);
            if (onFetched) onFetched();

            // 3. Pokud vše proběhlo OK, vypneme loading (bez abortu)
            useLoadingStore.setState({ isLoading: false, abortController: null });

        } catch (err: any) {
            // Ošetření zrušení požadavku
            if (err.name === 'AbortError') {
                console.log("Načítání bylo přerušeno uživatelem.");
            } else {
                console.error("Chyba při načítání dat:", err);
                // Tady bys mohl přidat nějaký toast s chybou
                useLoadingStore.setState({ isLoading: false, abortController: null });
            }
        }
    };

    return (
        <div>
            <BoundingBoxFilter />
            <DatetimeFilter />
            <DatasetFilter dataset={filters.dataset} setDataset={filters.setDataset} />

            <div className="fetch-button-wrapper">
                <button
                    className="btn btn-primary w-100 mt-2"
                    onClick={handleFetchFeatures}
                    disabled={isLoading}
                >
                    {isLoading ? "Fetching..." : "Fetch Features"}
                </button>
            </div>
        </div>
    );
}