import {useState} from "react";

export default function FiltersTab() {
    const [dataset, setDataset] = useState<"S1" | "S2">("S1");

    return (
        <div>
            <label>
                Dataset:
                <select value={dataset} onChange={(e) => setDataset(e.target.value as any)}>
                    <option value="S1">Sentinel 1</option>
                    <option value="S2">Sentinel 2</option>
                </select>
            </label>

            {dataset === "S1" && <div>{/* TODO: Sentinel 1 filters */}</div>}
            {dataset === "S2" && <div>{/* TODO: Sentinel 2 filters */}</div>}
        </div>
    );
}