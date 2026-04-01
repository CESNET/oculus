import {useEffect, useState} from "react";

/**
 * Debounce hook: returns value after specified delay
 * @param value - value to watch
 * @param delay - delay in milliseconds
 */
export function useDebounce<T>(value: T, delay: number): T {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const handler = setTimeout(() => setDebouncedValue(value), delay);

        return () => clearTimeout(handler);
    }, [value, delay]);

    return debouncedValue;
}
