import {useSentinel1Store} from "../../../store/useSentinel1Store";

export default function Sentinel1Filter() {
    const {sentinel1, toggleLevel, toggleSensingType, toggleProductType, togglePolarization} = useSentinel1Store();

    const levels = ["0", "1", "2"];
    const sensingTypes = ["IW", "EW", "SM", "WV"];
    const productTypes = ["SLC", "GRD"];
    const polarizations = ["HH", "HV", "VH", "VV"];

    return (
        <>
            {/*<h4>Sentinel-1 Filters</h4>*/}

            <div className="mb-3">
                <label>Levels</label>
                <div className="btn-group">
                    {levels.map(l => (
                        <button key={l} className={`btn ${sentinel1.levels.includes(l) ? "btn-primary" : "btn-outline-secondary"}`} onClick={() => toggleLevel(l)}>{l}</button>
                    ))}
                </div>
            </div>

            <div className="mb-3">
                <label>Sensing Types</label>
                <div className="btn-group">
                    {sensingTypes.map(s => (
                        <button key={s} className={`btn btn-sm ${sentinel1.sensingTypes.includes(s) ? "btn-primary" : "btn-outline-secondary"}`} onClick={() => toggleSensingType(s)}>{s}</button>
                    ))}
                </div>
            </div>

            <div className="mb-3">
                <label>Product Types</label>
                <div className="btn-group">
                    {productTypes.map(p => (
                        <button key={p} className={`btn ${sentinel1.productTypes.includes(p) ? "btn-primary" : "btn-outline-secondary"}`} onClick={() => toggleProductType(p)}>{p}</button>
                    ))}
                </div>
            </div>

            <div className="mb-3">
                <label>Polarization</label>
                <div className="btn-group">
                    {polarizations.map(p => (
                        <button key={p} className={`btn btn-sm ${sentinel1.polarizations.includes(p) ? "btn-primary" : "btn-outline-secondary"}`} onClick={() => togglePolarization(p)}>{p}</button>
                    ))}
                </div>
            </div>
        </>
    );
}
