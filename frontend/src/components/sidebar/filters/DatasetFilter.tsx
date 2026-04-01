import Sentinel1Filter from "./Sentinel1Filter";
import Sentinel2Filter from "./Sentinel2Filter";
import {Dataset} from "../../../types/datasets";

type DatasetFilterProps = {
    dataset: Dataset;
    setDataset: (d: Dataset) => void;
};

export default function DatasetFilter({dataset, setDataset}: DatasetFilterProps) {
    return (
        <div className="filter-section">
            <label>
                <h3>Dataset</h3>
                <select
                    value={dataset}
                    onChange={(e) => setDataset(e.target.value as Dataset)}
                >
                    <option value={Dataset.Sentinel1}>Sentinel-1</option>
                    <option value={Dataset.Sentinel2}>Sentinel-2</option>
                </select>
            </label>

            {dataset === Dataset.Sentinel1 && <Sentinel1Filter />}
            {dataset === Dataset.Sentinel2 && <Sentinel2Filter />}
        </div>
    );
}