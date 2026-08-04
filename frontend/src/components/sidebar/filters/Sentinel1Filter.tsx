import {useFiltersStore} from "../../../store/useFiltersStore";
import ButtonGroup from "../ButtonGroup.tsx";
import {Dataset} from "../../../types/datasets";
import {getAllFilterOptions} from "../../../utils/filterUtils.ts";

import type {Sentinel1Filter} from "../../../types/filters.ts";

export default function Sentinel1Filter() {
    const sentinel1 = useFiltersStore((s) => s.sentinel1);
    const toggleSentinel1 = useFiltersStore((s) => s.toggleSentinel1);

    const defaults = getAllFilterOptions(Dataset.Sentinel1) as Sentinel1Filter;

    return (
        <>
            <ButtonGroup
                multiple
                label="Levels"
                values={defaults.levels}
                selected={sentinel1.levels}
                onToggle={(v) => toggleSentinel1("levels", v)}
            />

            <ButtonGroup
                multiple
                label="Operational Modes"
                values={defaults.operationalModes}
                selected={sentinel1.operationalModes}
                onToggle={(v) => toggleSentinel1("operationalModes", v)}
            />

            <ButtonGroup
                multiple
                label="Product Types"
                values={defaults.productTypes}
                selected={sentinel1.productTypes}
                onToggle={(v) => toggleSentinel1("productTypes", v)}
            />

            <ButtonGroup
                multiple
                label="Polarizations"
                values={defaults.polarizations}
                selected={sentinel1.polarizations}
                onToggle={(v) => toggleSentinel1("polarizations", v)}
            />
        </>
    );
}