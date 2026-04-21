import { useState, useEffect } from "react";
import { searchLocation, moveMap } from "../../utils/mapUtils";
import { useDebounce } from "../../hooks/useDebounce";
import "./Navbar.css";

interface SearchBarProps {
    programmaticRef: React.MutableRefObject<boolean>;
}

export default function SearchField({ programmaticRef }: SearchBarProps) {
    const [searchQuery, setSearchQuery] = useState("");
    const [results, setResults] = useState<any[]>([]);
    const [showDropdown, setShowDropdown] = useState(false);

    const debouncedQuery = useDebounce(searchQuery, 300);

    useEffect(() => {
        if (!debouncedQuery) {
            setResults([]);
            setShowDropdown(false);
            return;
        }

        const fetchData = async () => {
            try {
                const data = await searchLocation(debouncedQuery);
                setResults(data);
                setShowDropdown(data.length > 0);
            } catch (err) {
                console.error(err);
                setResults([]);
                setShowDropdown(false);
            }
        };

        fetchData();
    }, [debouncedQuery]);

    const handleSelect = (item: any) => {
        const lat = parseFloat(item.lat);
        const lon = parseFloat(item.lon);

        programmaticRef.current = true;

        moveMap([lat, lon], 13, {
            duration: 1.2,
        });

        setSearchQuery(item.display_name);
        setResults([]);
        setShowDropdown(false);
    };

    return (
        <div className="search-form">
            <input
                type="text"
                className="search-input"
                placeholder="Search..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onFocus={() => setShowDropdown(results.length > 0)}
                onBlur={() => setTimeout(() => setShowDropdown(false), 150)}
            />

            <button
                type="button"
                className="search-button"
                onClick={() => results[0] && handleSelect(results[0])}
            >
                <i className="bi bi-search"></i>
            </button>

            {showDropdown && results.length > 0 && (
                <ul className="search-dropdown">
                    {results.map((item) => (
                        <li
                            key={item.place_id}
                            onClick={() => handleSelect(item)}
                        >
                            {item.display_name}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}