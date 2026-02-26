"use client";

import { useEffect, useState } from "react";
import "./globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from 'next/link';

/* =========================================
   1. READ MORE COMPONENT
   ========================================= */
const ReadMore = ({ text, limit = 60 }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  if (!text) return null;
  const words = text.split(/\s+/);
  
  if (words.length <= limit) {
    return <p style={{ textAlign: "justify", fontSize: "small" }}>{text}</p>;
  }

  return (
    <div style={{ textAlign: "justify", fontSize: "small" }}>
      <p style={{ display: "inline" }}>
        {isExpanded ? text : words.slice(0, limit).join(" ") + "..."}
      </p>
      <br />
      <center>
        <button
          className="read-more-btn"
          onClick={(e) => {
            e.stopPropagation(); 
            setIsExpanded(!isExpanded);
          }}
        >
          {isExpanded ? "Read Less" : "Read More"}
        </button>
      </center>
    </div>
  );
};

export default function Home() {
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

  const [slides, setSlides] = useState([]);
  const [testimonials, setTestimonials] = useState([]);
  const [registerLink, setRegisterLink] = useState("#");
  const [events, setEvents] = useState([]);
  const [currentSlideIndex, setCurrentSlideIndex] = useState(0);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/slides/`).then(res => res.json()).then(data => setSlides(data)).catch(err => console.log(err));
    fetch(`${API_BASE_URL}/api/testimonials/`).then(res => res.json()).then(data => setTestimonials(data)).catch(err => console.log(err));
    fetch(`${API_BASE_URL}/api/settings/`).then(res => res.json()).then(data => setRegisterLink(data.register_link)).catch(err => console.log(err));
    fetch(`${API_BASE_URL}/api/event/`).then(res => res.json()).then(data => setEvents(data)).catch(err => console.log(err));
  }, []);

  useEffect(() => {
    if (slides.length === 0) return;
    const interval = setInterval(() => {
      setCurrentSlideIndex(prev => prev === slides.length - 1 ? 0 : prev + 1);
    }, 8000);
    return () => clearInterval(interval);
  }, [slides]);

  const getImageUrl = (path) => {
  if (!path) return "/images/placeholder.jpg";
  
  // Agar path Cloudinary ka full URL hai (http se shuru ho raha hai)
  if (path.startsWith("http")) {
    return path; 
  }
  
  // Sirf purani local images ke liye
  return `${API_BASE_URL}${path}`;
};
  // Infinite Scroll Data Duplication
  const scrollingTestimonials = testimonials.length > 0 ? [...testimonials, ...testimonials] : [];
  const scrollingEvents = events.length > 0 ? [...events, ...events] : [];

  /* =========================================
     DYNAMIC SPEED LOGIC
     ========================================= */
  // Testimonials: 8 seconds per card (Slow for reading)
  const testimonialDuration = testimonials.length * 8; 
  
  // Events: 4 seconds per card (Fast for visual glimpses)
  const eventDuration = events.length * 4;

  return (
    <>
      <Navbar />

      {/* ================= SLIDER ================= */}
      <div className="slider-container">
        {slides.length > 0 ? (
          slides.map((s, i) => (
            <div key={i} className={`slide ${i === currentSlideIndex ? "active" : ""}`}>
              <img src={getImageUrl(s.image)} alt="Slide" className="slide-image" />
            </div>
          ))
        ) : (
          <div className="slide active">
            <div style={{ height: "400px", display: "flex", alignItems: "center", justifyContent: "center" }}>
              Loading Slides...
            </div>
          </div>
        )}
      </div>

      <div className="container">
        {/* ================= REGISTER ================= */}
        <div className="society-section" style={{ textAlign: "center"}}>
          <h2 className="section-title">Alumni Registration Society</h2>
          <p>Join the official network of Ram Lal Anand College. Stay updated with events, mentorship opportunities, and batch reunions.</p>
          <br />
          <a href={registerLink} target="_blank" className="btn-register" rel="noopener noreferrer">
            Register Now For Membership
          </a>
        </div>


    
        

        {/* ================= TESTIMONIALS ================= */}
        <div style={{ textAlign: "center", overflow: "hidden" }}>
          <h2 className="section-title">Alumni Testimonials</h2>
          {testimonials.length === 0 ? (
            <p>Loading testimonials...</p>
          ) : (
            <div className="scroll-container">
              <div 
                className="scroll-track" 
                style={{ animationDuration: `${testimonialDuration}s` }}
              >
                {scrollingTestimonials.map((t, i) => (
                 <div
  key={i}
  className="testimonial-card"
  style={{ 
    minWidth: "300px", 
    maxWidth: "300px",
    // Agar link hai toh pointer dikhega, warna normal cursor
    cursor: t.linkedin_url ? "pointer" : "default" 
  }} 
  onClick={() => {
    // Check: Agar link empty (""), null, ya undefined hai toh return ho jao
    if (!t.linkedin_url || t.linkedin_url === "#") {
      return; 
    }
    window.open(t.linkedin_url, "_blank");
  }}
>
                    <img src={getImageUrl(t.image)} alt={t.name} className="testimonial-image" />
                    <h3>{t.name}</h3>
                    <p>Batch {t.batch} | {t.course}</p><br />
                    <ReadMore text={t.text} limit={60} />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>


          <hr style={{border: "none", }}/>
        {/* ================= EVENTS ================= */}
        <div style={{ textAlign: "center", overflow: "hidden" }}>
          <h2 className="section-title">Event Glimpses</h2>
          {events.length === 0 ? (
            <p>Loading events...</p>
          ) : (
            <div className="scroll-container">
              <div 
                className="scroll-track" 
                style={{ animationDuration: `${eventDuration}s` }}
              >
                {scrollingEvents.map((event, i) => (
                  <Link href="/gallery" key={i} style={{ textDecoration: 'none' }}>
                    <div className="event-card" style={{ minWidth: "300px", cursor: "pointer" }}>
                      <img src={getImageUrl(event.cover)} alt={event.title} className="event-image" />
                      <div className="event-card-content">
                        <h3>{event.title}</h3>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      <Footer registerLink={registerLink} />
    </>
  );
}