"use client";
import React from 'react';
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function DonationPage() {
  const GFORM_LINK = process.env.NEXT_PUBLIC_DONATION_FORM_URL

  return (
    <>
      <Navbar />
      <div className="donation-wrapper">
        {/* Hero Section */}
        <section className="donation-hero">
          <div className="hero-overlay">
            <h1 className="hero-title">Support Your Alma Mater</h1>
            <p className="hero-subtitle">Make a Lasting Impact for Future Generations</p>
            <div className="gold-accent-line"></div>
          </div>
        </section>

        <div className="container-custom">
          {/* Main Message */}
          <section className="message-card shadow-lg">
            <div className="card-header">
              <h2>Dear Alumni,</h2>
              <div className="accent-line"></div>
            </div>
            <p className="main-text">
              Our college has always been more than a place of learning – it is a community, a home, 
              and a foundation for countless dreams. Today, you have the power to give back and 
              help shape the future of generations to come.
            </p>

            {/* Impact Grid */}
            <div className="impact-grid">
              <div className="impact-item">
                <div className="icon-circle">🎓</div>
                <h4>Scholarships</h4>
                <p>Financial aid for deserving students to pursue their dreams.</p>
              </div>
              <div className="impact-item">
                <div className="icon-circle">🏗️</div>
                <h4>Facilities</h4>
                <p>State-of-the-art infrastructure that inspires innovation.</p>
              </div>
              <div className="impact-item">
                <div className="icon-circle">🤝</div>
                <h4>Mentorship</h4>
                <p>Connecting alumni and students for career growth.</p>
              </div>
              <div className="impact-item">
                <div className="icon-circle">🌐</div>
                <h4>Network</h4>
                <p>Strengthening the bond of our global alumni community.</p>
              </div>
            </div>

            <div className="closing-message">
              <p>
                Every contribution, big or small, helps us continue our mission of excellence and 
                creates a lasting legacy. Your generosity fuels opportunities and nurtures talent.
              </p>
              <p className="call-to-action">Join us in making a difference today.</p>
            </div>

            {/* Donate Button */}
            <div className="button-wrapper">
              <a href={GFORM_LINK} target="_blank" rel="noopener noreferrer" className="donate-btn-main">
                Donate Now & Contribute
              </a>
              <p className="secure-text">🔒 You will be redirected to our official Google Form</p>
            </div>

            <div className="signature">
              <p>With gratitude,</p>
              <p className="team-name">The Alumni Association</p>
            </div>
          </section>
        </div>
      </div>
      <Footer />
    </>
  );
}