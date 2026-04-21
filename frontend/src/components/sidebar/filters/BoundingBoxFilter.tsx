import { useFiltersStore } from "../../../store/useFiltersStore.ts";

export default function BoundingBoxFilter() {
    const { bbox, setBbox } = useFiltersStore();

    return (
        <div className="filter-section">
            <h3>Bounding Box</h3>

            <div className="bbox-grid">
                <label>
                    North
                    <input
                        type="number"
                        value={bbox.north}
                        onChange={(e) =>
                            setBbox({ north: parseFloat(e.target.value) })
                        }
                    />
                </label>

                <label>
                    East
                    <input
                        type="number"
                        value={bbox.east}
                        onChange={(e) =>
                            setBbox({ east: parseFloat(e.target.value) })
                        }
                    />
                </label>

                <label>
                    South
                    <input
                        type="number"
                        value={bbox.south}
                        onChange={(e) =>
                            setBbox({ south: parseFloat(e.target.value) })
                        }
                    />
                </label>

                <label>
                    West
                    <input
                        type="number"
                        value={bbox.west}
                        onChange={(e) =>
                            setBbox({ west: parseFloat(e.target.value) })
                        }
                    />
                </label>
            </div>
        </div>
    );
}