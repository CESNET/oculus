import "./Navbar.css";

export default function Navbar() {
    return (
        <nav className="navbar">
            <div className="navbar-left">
                <img src="/logo.png" alt="Logo" className="navbar-logo"/>
                <h1 className="navbar-title">CESNET Oculus Visualization</h1>
            </div>

            <div className="navbar-right">
                <input
                    type="text"
                    className="navbar-search"
                    placeholder="Search..."
                />
            </div>
        </nav>
    );
}