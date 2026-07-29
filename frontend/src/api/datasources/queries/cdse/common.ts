import type {FiltersStore} from "../../../../store/useFiltersStore.ts";

export function buildSpatialFilter(filters: FiltersStore,): string {
    const {bbox} = filters;

    const polygon =
        `POLYGON((` +
        `${bbox.west} ${bbox.north},` +
        `${bbox.east} ${bbox.north},` +
        `${bbox.east} ${bbox.south},` +
        `${bbox.west} ${bbox.south},` +
        `${bbox.west} ${bbox.north}))`;

    return `OData.CSC.Intersects(area=geography'SRID=4326;${polygon}')`;
}

export function buildTemporalFilter(filters: FiltersStore,): string {
    const {datetime} = filters;

    const start = new Date(datetime.start).toISOString();
    const end = new Date(datetime.end).toISOString();

    return `ContentDate/Start ge ${start} and ContentDate/Start le ${end}`;
}
