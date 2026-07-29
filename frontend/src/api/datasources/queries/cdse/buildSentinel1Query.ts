import type {FiltersStore} from "../../../../store/useFiltersStore";
import {Dataset} from "../../../../types/datasets";
import {levelToApi} from "../../../../utils/filterUtils";

import {buildSpatialFilter, buildTemporalFilter} from "./common";

export function buildSentinel1Query(filters: FiltersStore): string {

    const parts: string[] = [];

    parts.push(buildSpatialFilter(filters));
    parts.push(buildTemporalFilter(filters));

    parts.push(`Collection/Name eq 'SENTINEL-1'`);

    const {sentinel1} = filters;

    if (sentinel1.operationalModes.length) {

        const sub = sentinel1.operationalModes.map(mode => (
                `Attributes/OData.CSC.StringAttribute/any(att:` +
                `att/Name eq 'operationalMode' and ` +
                `att/OData.CSC.StringAttribute/Value eq '${mode}')`
            )
        ).join(" or ");

        parts.push(`(${sub})`);
    }

    if (sentinel1.productTypes.length) {

        const sub = sentinel1.productTypes.map(type => (
                `Attributes/OData.CSC.StringAttribute/any(att:` +
                `att/Name eq 'productType' and ` +
                `att/OData.CSC.StringAttribute/Value eq '${type}')`
            )
        ).join(" or ");

        parts.push(`(${sub})`);
    }

    if (sentinel1.levels.length) {

        const sub = sentinel1.levels.map(level => (
                `Attributes/OData.CSC.StringAttribute/any(att:` +
                `att/Name eq 'processingLevel' and ` +
                `att/OData.CSC.StringAttribute/Value eq '${levelToApi(Dataset.Sentinel1, level)}')`
            )
        ).join(" or ");

        parts.push(`(${sub})`);
    }

    if (sentinel1.polarizations.length) {

        const polMap: Record<string, string[]> = {
            VV: ["VV", "VV&VH"],
            VH: ["VH", "VV&VH"],
            HH: ["HH", "HH&HV"],
            HV: ["HV", "HH&HV"],
        };

        const variants = Array.from(new Set(sentinel1.polarizations.flatMap(p => polMap[p] ?? [p])));

        const sub = variants.map(pol => (
                `Attributes/OData.CSC.StringAttribute/any(att:` +
                `att/Name eq 'polarisationChannels' and ` +
                `att/OData.CSC.StringAttribute/Value eq '${pol}')`
            )
        ).join(" or ");

        parts.push(`(${sub})`);
    }

    return parts.join(" and ");
}
