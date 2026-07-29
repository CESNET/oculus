import type {FiltersStore} from "../../store/useFiltersStore";

import {fetchProducts} from "./client/cdseClient";
import {buildSentinel1Query} from "./queries/cdse/buildSentinel1Query";
import {mapSentinel1ToFeature} from "./mappers/sentinel1Mapper";
import type {Feature} from "../../types/feature.ts";

export async function fetchSentinel1Features(
    filters: FiltersStore,
    signal?: AbortSignal,
): Promise<Feature[]> {

    const query = buildSentinel1Query(filters);

    console.log(query);

    const products = await fetchProducts(query, signal);

    return products.map(mapSentinel1ToFeature);
}
