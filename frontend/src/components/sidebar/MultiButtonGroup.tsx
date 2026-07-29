interface Props {
    label: string;
    values: string[];
    selected: string[];
    onToggle: (value: string) => void;
    small?: boolean;
}

export default function MultiButtonGroup({ label, values, selected, onToggle, small }: Props) {
    return (
        <div className="mb-3">
            <label>{label}</label>
            <div className={`btn-group${small ? " btn-group-sm" : ""}`}>
                {values.map((v) => (
                    <button
                        key={v}
                        className={`btn ${selected.includes(v) ? "btn-primary" : "btn-outline-secondary"}`}
                        onClick={() => onToggle(v)}
                    >
                        {v}
                    </button>
                ))}
            </div>
        </div>
    );
}