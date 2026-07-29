import {Dataset} from "../../../types/datasets";

import {parseWKTToCoordinates} from "../helpers/geometry";

import {
    getSentinel1Platform,
    getSentinel1Satellite,
    getSentinel1ProductType,
    getSentinel1Title
} from "../helpers/sentinel1";
import type {Feature} from "../../../types/feature.ts";

export function mapSentinel1ToFeature(item: any): Feature {
    return {
        id: item.Id,

        title: getSentinel1Title(item.Name),
        name: item.Name,

        dataset: Dataset.Sentinel1,

        platform: getSentinel1Platform(),
        satellite: getSentinel1Satellite(item.Name),
        productType: getSentinel1ProductType(item.Name),

        acquisitionDateTime: item.ContentDate?.Start ?? "",

        productUrl: `https://catalogue.dataspace.copernicus.eu/odata/v1/Products(${item.Id})`,

        geometry: {
            type: "Polygon",
            coordinates: item.Footprint ? [parseWKTToCoordinates(item.Footprint)] : [],
        },
    };
}
