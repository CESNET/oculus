import {useFiltersStore} from "../../../store/useFiltersStore";
import MultiButtonGroup from "./MultiButtonGroup";
import {Dataset} from "../../../types/datasets";
import {getAllOptions} from "../../../utils/filterUtils.ts";
import {type Sentinel1FilterState} from "../../../store/useFiltersStore";

export default function Sentinel1Filter() {
    const sentinel1 = useFiltersStore((s) => s.sentinel1);
    const toggleSentinel1 = useFiltersStore((s) => s.toggleSentinel1);

    const defaults = getAllOptions(Dataset.Sentinel1) as Sentinel1FilterState;

    return (
        <>
            <MultiButtonGroup
                label="Levels"
                values={defaults.levels}
                selected={sentinel1.levels}
                onToggle={(v) => toggleSentinel1("levels", v)}
            />

            <MultiButtonGroup
                label="Operational Modes"
                values={defaults.operationalModes}
                selected={sentinel1.operationalModes}
                onToggle={(v) => toggleSentinel1("operationalModes", v)}
            />

            <MultiButtonGroup
                label="Product Types"
                values={defaults.productTypes}
                selected={sentinel1.productTypes}
                onToggle={(v) => toggleSentinel1("productTypes", v)}
            />

            <MultiButtonGroup
                label="Polarizations"
                values={defaults.polarizations}
                selected={sentinel1.polarizations}
                onToggle={(v) => toggleSentinel1("polarizations", v)}
            />
        </>
    );
}