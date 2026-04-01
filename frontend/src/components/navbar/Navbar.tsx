import SearchField from "./SearchField";
import "./Navbar.css";

interface NavbarProps {
    programmaticRef: React.MutableRefObject<boolean>;
}

export default function Navbar({ programmaticRef }: NavbarProps) {
    return (
        <nav>
            <div className="left">
                <img src="/logo.png" alt="Logo" className="logo" />
                <h1 className="title">CESNET Oculus Visualization</h1>
            </div>

            <div className="right">
                <SearchField programmaticRef={programmaticRef} />
            </div>
        </nav>
    );
}