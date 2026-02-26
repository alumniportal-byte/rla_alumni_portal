"use client";
import React, { useState, useEffect } from 'react';
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function SuggestionPage() {
  const [suggestion_link, setSuggestionUrl] = useState("#");
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/suggestion-link/`)
      .then((res) => res.json())
      .then((data) => setSuggestionUrl(data.suggestion_link))
      .catch((err) => console.error("Error fetching suggestion link:", err));
  }, []);

  return (
    <>
      <Navbar />
      <div className="suggestion-wrapper">
        {/* Decorative Header */}
        <section className="suggestion-hero">
          <div className="hero-content">
            <h1 className="hero-title">Shape Our Future</h1>
            <p className="hero-subtitle">Your Wisdom is Our Best Guide</p>
            <div className="gold-accent-line"></div>
          </div>
        </section>

        <div className="container-main">
          <div className="content-card shadow-xl">
            <div className="text-section">
              <h2 className="greeting">Dear Alumni,</h2>
              <div className="gold-divider"></div>
              
              <p className="intro-text">
                As someone who has walked these corridors and achieved success in the world beyond, 
                you possess a unique perspective that can help us grow. Our college is a living 
                legacy, and your insights are the compass that helps us navigate new challenges.
              </p>

              <div className="why-guide-grid">
                <div className="guide-box">
                  <span className="box-icon">💡</span>
                  <h4>Industry Insights</h4>
                  <p>Tell us what skills the current industry demands so we can prepare our students.</p>
                </div>
                <div className="guide-box">
                  <span className="box-icon">🚀</span>
                  <h4>Innovation</h4>
                  <p>Suggest new initiatives, workshops, or clubs that can foster creativity.</p>
                </div>
                <div className="guide-box">
                  <span className="box-icon">✨</span>
                  <h4>Positive Feedback</h4>
                  <p>Share what we are doing right so we can strengthen those foundations further.</p>
                </div>
              </div>

              <div className="final-call">
                <p>
                  We invite you to share your constructive feedback and visionary suggestions. 
                  Whether it&#39;s a small improvement or a big idea, we are all ears. Let&#39;s work 
                  together to make our Alma Mater a beacon of excellence.
                </p>
              </div>

              {/* Action Button */}
              <div className="btn-container">
                <a 
                  href={suggestion_link} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="suggestion-submit-btn"
                >
                  Share Your Suggestions 📝
                </a>
                <p className="note">Clicking will open our official Feedback & Suggestion Google Form</p>
              </div>
            </div>

            <div className="closing-tag">
              <p>Together, We Grow.</p>
              <strong>The Alumni Association Team</strong>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
}