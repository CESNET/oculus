import {useState} from "react";
import {useFiltersStore} from "../../store/useFiltersStore";
import BoundingBoxFilter from "./filters/BoundingBoxFilter";
import DatetimeFilter from "./filters/DatetimeFilter";
import DatasetFilter from "./filters/DatasetFilter";
import {fetchFeaturesFromCDSE} from "../../api/cdse";

export default function FiltersTab() {
    const [dataset, setDataset] = useState<"S1" | "S2">("S1");
    const filters = useFiltersStore();
    const [loading, setLoading] = useState(false);
    const [features, setFeatures] = useState<any[]>([]);

    const handleFetchFeatures = async () => {
        setLoading(true);
        try {
            const fetched = await fetchFeaturesFromCDSE(filters, dataset); //Todo rozlišení na Sentinel/Landsat
            setFeatures(fetched);
            console.log("Fetched features:", fetched);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="sidebar">
            <div className="sidebar-panel">
                <BoundingBoxFilter />
                <DatetimeFilter />

                <DatasetFilter dataset={dataset} setDataset={setDataset} />

                <div className="fetch-button-wrapper">
                    <button className="btn btn-primary w-100 mt-2" onClick={handleFetchFeatures} disabled={loading}>
                        {loading ? "Fetching..." : "Fetch Features"}
                    </button>
                </div>
            </div>
        </div>
    );
}