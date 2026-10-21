import {
    SENTINEL2_SPECTRAL_BAND_OPTIONS,
    type Sentinel2SpectralBand,
} from "../../../types/visualization/sentinel2.ts";

interface Props {
    label: string;
    value: Sentinel2SpectralBand;
    onChange: (band: Sentinel2SpectralBand) => void;
}

export default function Sentinel2BandSelector({label, value, onChange}: Props) {
    return (
        <div className="mb-2">
            <label>{label}</label>

            <select
                className="form-select"
                value={value}
                onChange={(e) =>
                    onChange(e.target.value as Sentinel2SpectralBand)
                }
            >
                {SENTINEL2_SPECTRAL_BAND_OPTIONS.map((band) => (
                    <option
                        key={band.value}
                        value={band.value}
                    >
                        {band.label}
                    </option>
                ))}
            </select>
        </div>
    );
}