export interface ButtonOption<T extends string = string> {
    value: T;
    label: string;
}

type ButtonValue<T extends string> = T | ButtonOption<T>;

interface BaseProps<T extends string> {
    label: string;
    values: readonly ButtonValue<T>[];
    small?: boolean;
}

interface SingleProps<T extends string> extends BaseProps<T> {
    multiple?: false;
    selected: T;
    onChange: (value: T) => void;
}

interface MultiProps<T extends string> extends BaseProps<T> {
    multiple: true;
    selected: readonly T[];
    onToggle: (value: T) => void;
}

type Props<T extends string> = SingleProps<T> | MultiProps<T>;

function getValue<T extends string>(item: ButtonValue<T>): T {
    return typeof item === "string"
        ? item
        : item.value;
}

function getLabel<T extends string>(item: ButtonValue<T>): string {
    return typeof item === "string"
        ? item
        : item.label;
}

export default function ButtonGroup<T extends string>(props: Props<T>) {
    const {label, values, small} = props;

    const isSelected = (value: T) =>
        props.multiple
            ? props.selected.includes(value)
            : props.selected === value;

    const handleClick = (value: T) => {
        if (props.multiple) {
            props.onToggle(value);
        } else {
            props.onChange(value);
        }
    };

    return (
        <div className="mb-3">
            <label>{label}</label>

            <div
                className={`btn-group${small ? " btn-group-sm" : ""}`}
                role="group"
            >
                {values.map((item) => {
                    const value = getValue(item);
                    const buttonLabel = getLabel(item);

                    return (
                        <button
                            key={value}
                            type="button"
                            className={`btn ${
                                isSelected(value)
                                    ? "btn-primary"
                                    : "btn-outline-secondary"
                            }`}
                            onClick={() => handleClick(value)}
                        >
                            {buttonLabel}
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
