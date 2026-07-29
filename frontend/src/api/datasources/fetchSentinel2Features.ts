import type {FiltersStore} from "../../store/useFiltersStore";

import {fetchProducts} from "./client/cdseClient";
import {buildSentinel2Query} from "./queries/cdse/buildSentinel2Query";
import {mapSentinel2ToFeature} from "./mappers/sentinel2Mapper";
import type {Feature} from "../../types/feature.ts";

export async function fetchSentinel2Features(
    filters: FiltersStore,
    signal?: AbortSignal,
): Promise<Feature[]> {

    const query = buildSentinel2Query(filters);

    const products = await fetchProducts(query, signal);

    return products.map(mapSentinel2ToFeature);
}
