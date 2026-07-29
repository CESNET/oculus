import {Dataset} from "../../../types/datasets";

import {parseWKTToCoordinates} from "../helpers/geometry";

import {
    getSentinel2Platform,
    getSentinel2ProductType,
    getSentinel2Satellite,
} from "../helpers/sentinel2";
import type {Feature} from "../../../types/feature.ts";

export function mapSentinel2ToFeature(item: any): Feature {
    return {
        id: item.Id,

        title: `${getSentinel2Satellite(item.Name)} ${getSentinel2ProductType(item.Name)}`,
        name: item.Name,

        dataset: Dataset.Sentinel2,

        platform: getSentinel2Platform(),
        satellite: getSentinel2Satellite(item.Name),
        productType: getSentinel2ProductType(item.Name),

        acquisitionDateTime: item.ContentDate?.Start ?? "",

        productUrl: `https://catalogue.dataspace.copernicus.eu/odata/v1/Products(${item.Id})`,

        geometry: {
            type: "Polygon",
            coordinates: item.Footprint ? [parseWKTToCoordinates(item.Footprint)] : [],
        },
    };
}
