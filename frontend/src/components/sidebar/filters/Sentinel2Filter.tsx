import {useFiltersStore} from "../../../store/useFiltersStore";
import MultiButtonGroup from "../MultiButtonGroup.tsx";
import {Dataset} from "../../../types/datasets";
import {getAllFilterOptions} from "../../../utils/filterUtils.ts";

import type {Sentinel2Filter} from "../../../types/filters.ts";

export default function Sentinel2Filter() {
    const sentinel2 = useFiltersStore((s) => s.sentinel2);
    const toggleSentinel2 = useFiltersStore((s) => s.toggleSentinel2);
    const setSentinel2 = useFiltersStore((s) => s.setSentinel2);

    const defaults = getAllFilterOptions(Dataset.Sentinel2) as Sentinel2Filter;

    return (
        <>
            <div className="mb-3">
                <label>
                    Cloud Cover (%)

                    <input
                        type="number"
                        min={0}
                        max={100}
                        value={sentinel2.cloudCover ?? 100}
                        onChange={(e) =>
                            setSentinel2({
                                cloudCover: Number(e.target.value),
                            })
                        }
                    />

                    <input
                        type="range"
                        min={0}
                        max={100}
                        value={sentinel2.cloudCover ?? 100}
                        onChange={(e) =>
                            setSentinel2({
                                cloudCover: Number(e.target.value),
                            })
                        }
                    />
                </label>
            </div>

            <MultiButtonGroup
                label="Levels"
                values={defaults.levels}
                selected={sentinel2.levels}
                onToggle={(v) => toggleSentinel2("levels", v)}
            />
        </>
    );
}