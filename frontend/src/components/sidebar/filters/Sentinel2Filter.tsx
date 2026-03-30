import {useSentinel2Store} from "../../../store/useSentinel2Store";

export default function Sentinel2Filter() {
    const {sentinel2, toggleLevel, toggleBand, setCloudCover} = useSentinel2Store();
    const levels = ["0", "1A", "1B", "1C", "2A"];
    const bands = ["1", "2", "3", "4", "5", "6", "7", "8", "8A", "9", "10", "11", "12", "TCI"];

    return (
        <>
            {/*<h4>Sentinel-2 Filters</h4>*/}

            <div className="mb-3">
                <label>
                    Cloud Cover (%)
                    <input type="number" min={0} max={100} value={sentinel2.cloudCover}
                           onChange={e => setCloudCover(parseFloat(e.target.value))} />
                    <input type="range" min={0} max={100} value={sentinel2.cloudCover}
                           onChange={e => setCloudCover(parseFloat(e.target.value))} />
                </label>
            </div>

            <div className="mb-3">
                <label>Levels</label>
                <div className="btn-group">
                    {levels.map(l => (
                        <button key={l}
                                className={`btn ${sentinel2.levels.includes(l) ? "btn-primary" : "btn-outline-secondary"}`}
                                onClick={() => toggleLevel(l)}>{l}</button>
                    ))}
                </div>
            </div>

            <div className="mb-3">
                <label>Bands</label>
                <div className="btn-group">
                    {bands.map(b => (
                        <button key={b}
                                className={`btn btn-sm ${sentinel2.bands.includes(b) ? "btn-primary" : "btn-outline-secondary"}`}
                                onClick={() => toggleBand(b)}>{b}</button>
                    ))}
                </div>
            </div>
        </>
    );
}