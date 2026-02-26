"use client";
import React, { useState, useEffect } from 'react';
import { X, ChevronLeft, ChevronRight, Calendar } from 'lucide-react';
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function AlumniMeet() {
  const [events, setEvents] = useState([]);
  const [selectedPhotos, setSelectedPhotos] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/event/`)
      .then(res => res.json())
      .then(data => setEvents(data))
      .catch(err => console.error("Initial load error:", err));
  }, []);
  const getImageUrl = (path) => {
  if (!path) return "/images/placeholder.jpg";
  
  // 1. Agar path pehle se full URL hai (Cloudinary)
  if (typeof path === 'string' && (path.startsWith("http://") || path.startsWith("https://"))) {
    return path; 
  }
  
  // 2. Agar path relative hai (Local Media)
  // Ensure path starts with /
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${API_BASE_URL}${cleanPath}`;
};
  const openGallery = (eventId) => {
    fetch(`${API_BASE_URL}/api/event/${eventId}/`)
      .then(res => res.json())
      .then(photos => {
        if (photos && photos.length > 0) {
          setSelectedPhotos(photos);
          setCurrentIndex(0);
        } else {
          alert("Is folder mein koi photos nahi hain!");
        }
      })
      .catch(err => console.error("Gallery fetch error:", err));
  };

  return (
    <>
      <Navbar />
      <div className="alumni-page-wrapper">
  {/* Header Section (Same as Directory/Wall of Fame) */}
  <header className="gallery-hero">
    <div className="hero-overlay">
      <h1 className="hero-title">Meet Gallery</h1>
      <p className="hero-subtitle">CAPTURING TIMELESS MOMENTS</p>
      <div className="gold-accent-line"></div>
    </div>
  </header>

  <div className="meet-wrapper">
    <div className="meet-header">
      <div className="directory-info-text">
        <p className="page-description">
          Relive the memories of our past gatherings. Click on a folder to view the full event gallery.
        </p>
      </div>
    </div>

    <div className="folder-container">
      {events.map((event, idx) => (
        <div key={event.id || idx} className="folder-card" onClick={() => openGallery(event.id)}>
          <div className="folder-tab"></div>
          <div className="folder-body">
            <img src={getImageUrl(event.cover)} className="folder-thumb" alt="cover" />
            <div className="folder-info">
              <h3 className="folder-name">{event.title}</h3>
            </div>
          </div>
        </div>
      ))}
    </div>
  </div>

        {selectedPhotos && (
          <div className="lightbox-overlay">
            <button className="close-btn" onClick={() => setSelectedPhotos(null)}>
              <X size={35} />
            </button>
            <button className="nav-btn prev" onClick={() => setCurrentIndex((currentIndex - 1 + selectedPhotos.length) % selectedPhotos.length)}>
              <ChevronLeft size={45} />
            </button>

            <div className="lightbox-content">
              {selectedPhotos.map((photoObj, idx) => (
  <div key={`gallery-img-${idx}`} style={{ display: idx === currentIndex ? "block" : "none" }}>
    <img 
      src={getImageUrl(photoObj.image || photoObj.url || photoObj)} // <-- .url add kiya kyunki backend ab object bhej raha hai
      className="full-img" 
      alt={`Gallery ${idx}`}
      onError={(e) => { e.target.src = "https://via.placeholder.com/800"; }}
    />
  </div>
))}
              <p className="img-counter">{currentIndex + 1} / {selectedPhotos.length}</p>
            </div>

            <button 
              className="nav-btn next" 
              onClick={() => setCurrentIndex((currentIndex + 1) % selectedPhotos.length)}
            >
              <ChevronRight size={45} />
            </button>
          </div>
        )}
      </div> {/* Fixed the stray closing div here */}
      <Footer />
    </>
  );
}