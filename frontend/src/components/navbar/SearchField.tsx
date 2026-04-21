import { useState, useEffect, useRef } from "react";
import { searchLocation, moveMap } from "../../utils/mapUtils";
import { useDebounce } from "../../hooks/useDebounce";
import "./Navbar.css";

interface SearchBarProps {
    /** External flag used to prevent map/search conflicts during programmatic navigation */
    programmaticRef: React.MutableRefObject<boolean>;
}

/**
 * SearchField
 *
 * A location autocomplete search component with:
 * - debounced API search
 * - keyboard navigation
 * - map integration
 * - race-condition safe async handling
 * - auto-select-on-focus UX behavior
 */
export default function SearchField({ programmaticRef }: SearchBarProps) {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<any[]>([]);
    const [activeIndex, setActiveIndex] = useState(-1);
    const [isSelecting, setIsSelecting] = useState(false);
    const [isFocused, setIsFocused] = useState(false);

    const inputRef = useRef<HTMLInputElement>(null);
    const listRef = useRef<HTMLUListElement>(null);

    const requestIdRef = useRef(0);
    const suppressOpenRef = useRef(false);
    const ignoreFocusRef = useRef(false);
    const hasUserFocusedRef = useRef(false);

    const debouncedQuery = useDebounce(query, 300);

    // -----------------------------
    // SEARCH (race-safe)
    // -----------------------------
    useEffect(() => {
        const q = debouncedQuery.trim();

        if (!q || isSelecting || suppressOpenRef.current) {
            setResults([]);
            setActiveIndex(-1);
            return;
        }

        const currentRequest = ++requestIdRef.current;

        (async () => {
            const data = await searchLocation(q);

            // ignore stale responses
            if (currentRequest !== requestIdRef.current) return;

            setResults(data);
            setActiveIndex(-1);
        })();
    }, [debouncedQuery, isSelecting]);

    // -----------------------------
    // DROPDOWN VISIBILITY (single source of truth)
    // -----------------------------
    const showDropdown =
        isFocused &&
        !isSelecting &&
        !suppressOpenRef.current &&
        results.length > 0;

    // -----------------------------
    // AUTO-SCROLL ACTIVE ITEM
    // -----------------------------
    useEffect(() => {
        if (activeIndex < 0) return;

        const el = listRef.current?.children[activeIndex] as HTMLElement;
        el?.scrollIntoView({ block: "nearest" });
    }, [activeIndex]);

    // -----------------------------
    // SELECT ITEM + MAP ACTION
    // -----------------------------
    const selectItem = (item: any) => {
        const lat = parseFloat(item.lat);
        const lon = parseFloat(item.lon);

        setIsSelecting(true);

        suppressOpenRef.current = true;
        ignoreFocusRef.current = true;

        requestIdRef.current++;
        programmaticRef.current = true;

        moveMap([lat, lon], 13, { duration: 1.2 });

        setQuery(item.display_name);
        setResults([]);
        setActiveIndex(-1);

        setTimeout(() => {
            setIsSelecting(false);
            suppressOpenRef.current = false;
            ignoreFocusRef.current = false;
            programmaticRef.current = false;
        }, 500);
    };

    // -----------------------------
    // INPUT HANDLERS
    // -----------------------------

    /**
     * Handles input focus.
     * Ensures dropdown opens only after real user interaction.
     */
    const handleFocus = () => {
        if (ignoreFocusRef.current) return;

        setIsFocused(true);

        // mark that user interacted with input
        hasUserFocusedRef.current = true;
    };

    /**
     * Handles input blur (closes dropdown contextually).
     */
    const handleBlur = () => {
        setIsFocused(false);
    };

    /**
     * Selects all text on first user interaction for faster editing UX.
     */
    const handleSelectAll = () => {
        inputRef.current?.select();
    };

    /**
     * Updates query and resets results if empty.
     */
    const handleChange = (value: string) => {
        setQuery(value);

        if (!value.trim()) {
            setResults([]);
            setActiveIndex(-1);
        }
    };

    /**
     * Keyboard navigation (arrow keys, enter, escape)
     */
    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (!showDropdown) return;

        if (e.key === "ArrowDown") {
            e.preventDefault();
            setActiveIndex(prev => (prev + 1) % results.length);
        }

        if (e.key === "ArrowUp") {
            e.preventDefault();
            setActiveIndex(prev => (prev - 1 + results.length) % results.length);
        }

        if (e.key === "Enter") {
            e.preventDefault();

            const item = results[activeIndex >= 0 ? activeIndex : 0];
            if (item) selectItem(item);
        }

        if (e.key === "Escape") {
            setResults([]);
            setActiveIndex(-1);
        }
    };

    // -----------------------------
    // UI
    // -----------------------------
    return (
        <div className="search-form">
            <input
                ref={inputRef}
                type="text"
                className={`search-input ${showDropdown ? "active" : ""}`}
                placeholder="Search..."
                value={query}
                onChange={(e) => handleChange(e.target.value)}
                onFocus={handleFocus}
                onBlur={handleBlur}
                onClick={handleSelectAll}
                onKeyDown={handleKeyDown}
            />

            <button
                type="button"
                className="search-button"
                onClick={() => results[0] && selectItem(results[0])}
            >
                <i className="bi bi-search"></i>
            </button>

            {showDropdown && (
                <ul className="search-dropdown" ref={listRef}>
                    {results.map((item, idx) => (
                        <li
                            key={item.place_id}
                            title={item.display_name}
                            className={idx === activeIndex ? "active" : ""}
                            onMouseDown={() => selectItem(item)}
                        >
                            {item.display_name}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}