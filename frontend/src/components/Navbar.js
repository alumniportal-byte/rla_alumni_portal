"use client";
import Link from "next/link";
import { useEffect, useState,Suspense } from "react";
import { usePathname, useSearchParams } from "next/navigation";

function NavbarContent() {
  const [suggestion_link, setSuggestionUrl] = useState("#");
  const [menuOpen, setMenuOpen] = useState(false);
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const currentTab = searchParams?.get("tab") || null;

  useEffect(() => {
    // Fetching the admin-editable suggestion link
    fetch(`${API_BASE_URL}/api/suggestion-link/`)
      .then((res) => res.json())
      .then((data) => setSuggestionUrl(data.suggestion_link))
      .catch((err) => console.error("Error fetching suggestion link:", err));
  }, []);

  useEffect(() => {
    setMenuOpen(false);
  }, [pathname]);

  return (
    <>
      {/* ================= HEADER ================= */}
      <header>
        <div className="header-container">
          <img src="/images/rla_logo.jpg" className="college-logo" alt="RLA Logo" height={500} width={500} />
          <div className="header-text">
            <h1>Alumni Association (Reg.)</h1>
            <h2>Ram Lal Anand College</h2>
            <p>University of Delhi | NAAC &apos;A&apos; Grade</p>
            <p>Registration No. SOCIETY/WEST/2019/8902461</p>
          </div>
          <img src="/images/du_logo.png" className="uni-logo" alt="DU Logo" height={500} width={500} />
        </div>
      </header>

      {/* ================= NAVBAR ================= */}
      <nav>
        <button className="nav-toggle" aria-label="Toggle navigation" onClick={() => setMenuOpen(!menuOpen)}>☰</button>
  <div className={`dropdown-main ${menuOpen ? "show" : ""}`}>
    <Link href="/" className={pathname === "/" ? "active" : ""}>Home</Link>
    
    <div className="dropdown-parent">
      <b><span style={{ color: "white", cursor: "pointer", padding: "14px 20px" }}>About Us ▾</span></b>
      <div className="dropdown-menu">
        <Link href="/about?tab=patron" className={pathname === "/about" && currentTab === "patron" ? "active" : ""}>Patron&apos;s Message</Link>
        <div className="nested-dropdown">
          <b><span className="nested-trigger">About College ▸</span></b>
          <div className="nested-menu">
            <Link href="/about?tab=college" className={pathname === "/about" && currentTab === "college" ? "active" : ""}>History & Heritage</Link>
            <Link href="/about?tab=faculty" className={pathname === "/about" && currentTab === "faculty" ? "active" : ""}>Teaching Faculty</Link>
            <Link href="/about?tab=staff" className={pathname === "/about" && currentTab === "staff" ? "active" : ""}>Non-Teaching Staff</Link>
            <Link href="/docs/PENSIONER DETAIL ( RETIRED ).pdf" target="_blank" rel="noopener noreferrer" title="public\docs\PENSIONER DETAIL ( RETIRED ).pdf" className={pathname === "/about" && currentTab === "Retired Teaching & Non-Teaching staff " ? "active" : ""}>Retired Teaching & Non-Teaching staff</Link>
          </div>
        </div>  
        <Link href="/about?tab=association" className={pathname === "/about" && currentTab === "association" ? "active" : ""}>Alumni Association</Link>
        <Link href="/about?tab=bearers" className={pathname === "/about" && currentTab === "bearers" ? "active" : ""}>Alumni Association Office Bearers</Link>
        <Link href="/about?tab=committee" className={pathname === "/about" && currentTab === "committee" ? "active" : ""}>College Alumni Committee</Link>
        <Link href="/about?tab=preamble" className={pathname === "/about" && currentTab === "preamble" ? "active" : ""}>Preamble</Link>
      </div>
    </div>

    <Link href="/committee" className={pathname === "/committee" ? "active" : ""}>Alumni Events</Link>
    <Link href="/alumni" className={pathname === "/alumni" ? "active" : ""}>Registered Alumni</Link>
    <Link href="/distinguished" className={pathname === "/distinguished" ? "active" : ""}>Wall of Fame</Link>
    <Link href="/gallery" className={pathname === "/gallery" ? "active" : ""}>Alumni Meet</Link>
    <Link href="/donation" className={pathname === "/donation" ? "active" : ""}>Donation</Link>
    <Link href="/suggestion" className={pathname === "/suggestion" ? "active" : ""}>Guide Us</Link>
  </div>
</nav>
    </>
  );
}
export default function Navbar() {
  return (
    <Suspense fallback={<div></div>}>
      <NavbarContent />
    </Suspense>
  );
}
