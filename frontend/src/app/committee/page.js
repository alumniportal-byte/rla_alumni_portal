"use client";
import React, { useState, useEffect } from 'react';
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer"; 

export default function AlumniEventsPage() {
  const [groupedData, setGroupedData] = useState({});
  const [activeAccordion, setActiveAccordion] = useState(null);
  const [loading, setLoading] = useState(true);

  const API_BASE = "http://127.0.0.1:8000";

  useEffect(() => {
    fetch(`${API_BASE}/api/grouped-events/`)
      .then(res => res.json())
      .then(data => {
        setGroupedData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Fetch Error:", err);
        setLoading(false);
      });
  }, []);

  const toggleAccordion = (key) => {
    setActiveAccordion(activeAccordion === key ? null : key);
  };

  return (
    <>
      <Navbar />
      <div className="alumni-event-wrapper">
        {/* Donation/Suggestion jaisa Hero Section */}
        <section className="event-hero">
          <div className="hero-overlay">
            <h1 className="hero-title">Alumni Events</h1>
            <p className="hero-subtitle">Reliving Memories, Building Connections</p>
            <div className="gold-accent-line"></div>
          </div>
        </section>

        <div className="container-main">
          {/* Main Card Jo Donation Page jaisa dikhega */}
          <section className="main-content-card shadow-2xl">
            
            <div className="intro-box">
              <p>
                Our events are a platform for alumni to reconnect, share their success stories, 
                and guide the next generation. Explore our past and upcoming initiatives 
                categorized by sessions.
              </p>
            </div>

            {loading ? (
              <div className="loader-text">Loading events...</div>
            ) : (
              <div className="category-container">
                {Object.entries(groupedData).map(([category, sessions]) => (
                  <div key={category} className="category-group">
                    {/* Category Label like your image */}
                    <div className="cat-header-badge">
                      <span>{category}</span>
                    </div>

                    <div className="session-stack">
                      {Object.entries(sessions).map(([session, events]) => {
                        const itemKey = `${category}-${session}`;
                        const isOpen = activeAccordion === itemKey;

                        return (
                          <div key={session} className={`session-accordion ${isOpen ? 'is-open' : ''}`}>
                            <div className="session-trigger" onClick={() => toggleAccordion(itemKey)}>
                              <span className="session-label">Academic Session: {session}</span>
                              <div className="trigger-right">
                                <span className="badge-count">{events.length} Events</span>
                                <span className="chevron">{isOpen ? '−' : '+'}</span>
                              </div>
                            </div>

                            {isOpen && (
                              <div className="events-display-grid animate-fadeIn">
                                {events.map(event => (
                                  <div key={event.id} className="event-item-card">
                                    <div className="img-container">
                                      <img src={event.image} alt={event.title} />
                                      <div className="date-overlay">{event.date}</div>
                                    </div>
                                    <div className="details-container">
                                      <h4 className="etitle">{event.title}</h4>
                                      <p className="e-org">Organized by {event.organized_by}</p>
                                      <div className="e-info-row">
                                        <p><strong>Speaker:</strong> {event.resource_person}</p>
                                        <p><strong>Batch:</strong> {event.batch}</p>
                                      </div>
                                      {event.report && (
                                        <a href={event.report} target="_blank" className="view-report-link">
                                          Download Report (PDF)
                                        </a>
                                      )}
                                    </div>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>
      </div>
      <Footer />
    </>
  );
}