"use client";
import React, { useState, useEffect, useMemo } from 'react';
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import "../globals.css";

export default function RegisteredAlumni() {
  const [alumni, setAlumni] = useState([]);
  const [registerLink, setRegisterLink] = useState("#");
  const [loading, setLoading] = useState(true);
  
  // Filter States
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCourse, setSelectedCourse] = useState("");
  const [selectedBatch, setSelectedBatch] = useState("");
  const [selectedStatus, setSelectedStatus] = useState(""); 

  // Pagination States
  const [currentPage, setCurrentPage] = useState(1);
  const entriesPerPage = 100;

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

  // --- Initial Data Fetch ---
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [settingsRes, alumniRes] = await Promise.all([
          fetch(`${API_BASE_URL}/api/settings/`),
          fetch(`${API_BASE_URL}/api/alumni/`)
        ]);
        
        const settingsData = await settingsRes.json();
        const alumniData = await alumniRes.json();
        
        setRegisterLink(settingsData.register_link || "#");
        if (Array.isArray(alumniData)) {
          setAlumni(alumniData);
        }
      } catch (err) {
        console.error("Fetch error:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // --- Live Filter Logic (Using useMemo for performance & to avoid Red Errors) ---
  const filteredAlumni = useMemo(() => {
    return alumni.filter(person => {
      const nameMatch = (person.name || "").toLowerCase().includes(searchTerm.toLowerCase());
      const courseMatch = selectedCourse === "" || person.course === selectedCourse;
      const batchMatch = selectedBatch === "" || person.batch === selectedBatch;
      
      let statusMatch = true;
      if (selectedStatus === "reg") statusMatch = person.is_registered === true;
      if (selectedStatus === "not") statusMatch = person.is_registered === false;

      return nameMatch && courseMatch && batchMatch && statusMatch;
    });
  }, [searchTerm, selectedCourse, selectedBatch, selectedStatus, alumni]);

  // Reset page to 1 when filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, selectedCourse, selectedBatch, selectedStatus]);

  const handleReset = () => {
    setSearchTerm("");
    setSelectedCourse("");
    setSelectedBatch("");
    setSelectedStatus("");
    setCurrentPage(1);
  };

  // --- Pagination Logic ---
  const indexOfLastEntry = currentPage * entriesPerPage;
  const indexOfFirstEntry = indexOfLastEntry - entriesPerPage;
  const currentEntries = filteredAlumni.slice(indexOfFirstEntry, indexOfLastEntry);
  const totalPages = Math.ceil(filteredAlumni.length / entriesPerPage);

  // Pagination Numbers (Google Style)
  const pageNumbers = [];
  let startPage = Math.max(1, currentPage - 2);
  let endPage = Math.min(totalPages, startPage + 4);
  if (endPage - startPage < 4) startPage = Math.max(1, endPage - 4);
  for (let i = startPage; i <= endPage; i++) { if(i > 0) pageNumbers.push(i); }

  return (
    <>
      <Navbar />
<div className="alumni-page-wrapper">
  {/* Hero Section */}
  <header className="directory-hero">
    <div className="hero-overlay">
      <h1 className="hero-title">Alumni Directory</h1>
      <p className="hero-subtitle">CELEBRATING OUR GLOBAL NETWORK</p>
      <div className="gold-accent-line"></div>
    </div>
  </header>

  <div className="container-main-wide"> {/* Use this class for bigger width */}
    <div className="directory-card">
      
      <div className="directory-info-text">
        <p>Data update in progress. Kindly excuse any inconsistency.</p>
      </div>

      {/* --- Filters in Single Line --- */}
      <div className="alumni-filter-row">
        <input 
          type="text" 
          placeholder="Search by Name..." 
          className="search-input"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        
        <select className="filter-select" value={selectedCourse} onChange={(e) => setSelectedCourse(e.target.value)}>
          <option value="">All Courses</option>
          {[...new Set(alumni.map(a => a.course))].filter(Boolean).sort().map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>

        <select className="filter-select" value={selectedBatch} onChange={(e) => setSelectedBatch(e.target.value)}>
          <option value="">All Batches</option>
          {[...new Set(alumni.map(a => a.batch))].filter(Boolean).sort((a,b) => b-a).map(b => (
            <option key={b} value={b}>{b}</option>
          ))}
        </select>

        <select className="filter-select" value={selectedStatus} onChange={(e) => setSelectedStatus(e.target.value)}>
          <option value="">All Status</option>
          <option value="reg">Registered</option>
          <option value="not">Not Registered</option>
        </select>

        <button className="reset-action-btn" onClick={handleReset}>Reset</button>
      </div>

      {/* --- Table Section --- */}
      <div className="table-responsive-wrapper">
        {loading ? (
          <div className="custom-loader">Fetching Directory Data...</div>
        ) : (
          <>
            <table className="alumni-main-table">
              <thead>
                <tr>
                  <th>S.No</th>
                  <th>Full Name</th>
                  <th>Course</th>
                  <th>Batch</th>
                  <th>Registration Status</th>
                </tr>
              </thead>
              <tbody>
                {currentEntries.length > 0 ? (
                  currentEntries.map((a, index) => (
                    <tr key={a.id || index}>
                      <td>{indexOfFirstEntry + index + 1}</td>
                      <td className="name-cell">{a.name}</td>
                      <td className="course-cell">{a.course}</td>
                      <td className="batch-cell">{a.batch}</td>
                      <td>
                        {a.is_registered ? (
                          <span className="status-reg-badge">✓ Registered</span>
                        ) : (
                          <div className="not-reg-container">
                            <span className="status-not-badge">Not Registered</span>
                            <a href={registerLink} target="_blank" rel="noopener noreferrer" className="quick-link">Click here to Register</a>
                          </div>
                        )}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr><td colSpan="5" className="no-data-msg">No results found matching your criteria.</td></tr>
                )}
              </tbody>
            </table>

            {/* --- Pagination Fixed Location --- */}
            <div className="pagination-footer">
              <button 
                disabled={currentPage === 1} 
                onClick={() => setCurrentPage(prev => prev - 1)} 
                className="nav-action-btn"
              >
                ← Prev
              </button>
              
              <div className="page-numbers-group">
                {pageNumbers.map(number => (
                  <button 
                    key={number} 
                    onClick={() => setCurrentPage(number)} 
                    className={`num-btn ${currentPage === number ? 'active-num' : ''}`}
                  >
                    {number}
                  </button>
                ))}
              </div>

              <button 
                disabled={currentPage === totalPages} 
                onClick={() => setCurrentPage(prev => prev + 1)} 
                className="nav-action-btn"
              >
                Next →
              </button>
            </div>
          </>
        )}
      </div>  
    </div>
  </div>
</div>
      <Footer registerLink={registerLink} />
    </>
  );
}