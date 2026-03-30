// DatasetFilter.tsx
import Sentinel1Filter from "./Sentinel1Filter";
import Sentinel2Filter from "./Sentinel2Filter";

type DatasetFilterProps = {
    dataset: "S1" | "S2";
    setDataset: (d: "S1" | "S2") => void;
};

export default function DatasetFilter({dataset, setDataset}: DatasetFilterProps) {
    return (
        <div className="filter-section">
            <label>
                <h3>Dataset</h3>
                <select value={dataset} onChange={(e) => setDataset(e.target.value as "S1" | "S2")}>
                    <option value="S1">Sentinel-1</option>
                    <option value="S2">Sentinel-2</option>
                </select>
            </label>

            {dataset === "S1" && <Sentinel1Filter />}
            {dataset === "S2" && <Sentinel2Filter />}
        </div>
    );
}
