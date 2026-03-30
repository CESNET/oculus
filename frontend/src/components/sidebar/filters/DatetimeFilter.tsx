import { useFiltersStore } from "../../../store/useFiltersStore";

export default function DatetimeFilter() {
    const { datetime, setDatetime } = useFiltersStore();

    // 👉 lokální datum bez UTC posunu
    const today = new Date().toLocaleDateString("sv-SE"); // YYYY-MM-DD

    // 👉 z ISO stringu vezmeme jen datum
    const displayStart = datetime.start.slice(0, 10);
    const displayEnd = datetime.end.slice(0, 10);

    const handleStartChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        if (!value) return;

        // zákaz budoucnosti
        if (value > today) return;

        setDatetime({ start: value });
    };

    const handleEndChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        if (!value) return;

        // zákaz budoucnosti
        if (value > today) return;

        setDatetime({ end: value });
    };

    return (
        <div className="filter-section">
            <h3>Date Range</h3>

            <div className="input-pair">
                <label>
                    Start:
                    <input type="date" value={displayStart} max={displayEnd} onChange={handleStartChange}/>
                </label>

                <label>
                    End:
                    <input type="date" value={displayEnd} min={displayStart} max={today} onChange={handleEndChange}/>
                </label>
            </div>
        </div>
    );
}