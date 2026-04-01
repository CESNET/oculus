import Navbar from "../components/navbar/Navbar";

interface NavbarLayoutProps {
    programmaticRef: React.MutableRefObject<boolean>;
}

export default function NavbarLayout({programmaticRef}: NavbarLayoutProps) {
    return <Navbar programmaticRef={programmaticRef}/>;
}