import type {FiltersStore} from "../../../../store/useFiltersStore.ts";
import {Dataset} from "../../../../types/datasets";
import {levelToApi} from "../../../../utils/filterUtils";

import {
    buildSpatialFilter,
    buildTemporalFilter,
} from "./common";

export function buildSentinel2Query(filters: FiltersStore): string {

    const parts: string[] = [];

    parts.push(buildSpatialFilter(filters));
    parts.push(buildTemporalFilter(filters));

    parts.push(`Collection/Name eq 'SENTINEL-2'`);

    const {sentinel2} = filters;

    if (sentinel2.levels.length) {

        const sub = sentinel2.levels.map((level: any) => (
                `Attributes/OData.CSC.StringAttribute/any(att:` +
                `att/Name eq 'productType' and ` +
                `att/OData.CSC.StringAttribute/Value eq '${levelToApi(Dataset.Sentinel2, level)}')`
            )
        ).join(" or ");

        parts.push(`(${sub})`);
    }

    if (sentinel2.cloudCover != null) {
        parts.push(
            `Attributes/OData.CSC.DoubleAttribute/any(att:` +
            `att/Name eq 'cloudCover' and ` +
            `att/OData.CSC.DoubleAttribute/Value le ${sentinel2.cloudCover.toFixed(2)})`
        );
    }

    return parts.join(" and ");
}
