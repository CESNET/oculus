import {useState} from "react";
import {useFiltersStore} from "../../store/useFiltersStore";
import BoundingBoxFilter from "./filters/BoundingBoxFilter";
import DatetimeFilter from "./filters/DatetimeFilter";
import DatasetFilter from "./filters/DatasetFilter";
import {fetchFeatures} from "../../api/fetchFeatures";
import {useFeaturesStore} from "../../store/useFeaturesStore";
import {getEffectiveFilters} from "../../utils/filterUtils.ts";

interface FiltersTabProps {
    onFetched?: () => void;
}

export default function FiltersTab({onFetched}: FiltersTabProps) {
    const filters = useFiltersStore();
    const [loading, setLoading] = useState(false);
    const setFeatures = useFeaturesStore((state) => state.setFeatures);

    const handleFetchFeatures = async () => {
        setLoading(true);

        const effectiveFilters = getEffectiveFilters(filters, filters.dataset);
        useFiltersStore.getState().setFilters({
            sentinel1: effectiveFilters.sentinel1,
            sentinel2: effectiveFilters.sentinel2,
        });

        try {
            const fetched = await fetchFeatures(effectiveFilters, filters.dataset);
            setFeatures(fetched);
            if (onFetched) onFetched();
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <BoundingBoxFilter />
            <DatetimeFilter />
            <DatasetFilter dataset={filters.dataset} setDataset={filters.setDataset} />

            <div className="fetch-button-wrapper">
                <button className="btn btn-primary w-100 mt-2" onClick={handleFetchFeatures} disabled={loading}>
                    {loading ? "Fetching..." : "Fetch Features"}
                </button>
            </div>
        </div>
    );
}