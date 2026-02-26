"use client";
import React, { useState, useEffect } from 'react';
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { 
  Shield, Film, Tv, GraduationCap, Building2, Scale, 
  Stethoscope, Landmark, Atom, Trophy, Users, ChevronLeft 
} from 'lucide-react';

const iconMap = {
  "Defence": <Shield size={20} />,
  "Cinema & Entertainment": <Film size={20} />,
  "Electronic & Print Media": <Tv size={20} />,
  "Educationist": <GraduationCap size={20} />,
  "Industrialist / Entrepreneur": <Building2 size={20} />,
  "Legal Luminaries": <Scale size={20} />,
  "Medical & Healthcare": <Stethoscope size={20} />,
  "Politician": <Landmark size={20} />,
  "Science & Research": <Atom size={20} />,
  "Sports Veterans": <Trophy size={20} />,
  "Government Officials": <Users size={20} />
};

export default function DistinguishedAlumni() {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [members, setMembers] = useState([]);
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/alumni-categories/`)
      .then(res => res.json())
      .then(data => setCategories(data));
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
  const handleCategoryClick = (cat) => {
    setSelectedCategory(cat);
    fetch(`${API_BASE_URL}/api/wall-of-fame/${cat.id}/`)
      .then(res => res.json())
      .then(data => setMembers(data));
  };

  return (
    <>
      <Navbar />
         <div className="alumni-page-wrapper">
  <header className="wall-fame-hero">
    <div className="hero-overlay">
      <h1 className="hero-title">Wall of Fame</h1>
      <p className="hero-subtitle">HONOURING OUR ALUMNI</p>
      <div className="gold-accent-line"></div>
    </div><br />
  </header>
        <div className="wall-fame-wrapper">
          <div className="wall-header">
            
            <h2 className="section-title">
              {selectedCategory ? selectedCategory.name : "Find Alumni in Your Field"}</h2>
          </div>
          
          {!selectedCategory ? (
            <div className="category-flex-container">
              {categories.map(cat => (
                <div key={cat.id} className="cat-card-premium" onClick={() => handleCategoryClick(cat)}>
                  <span className="cat-icon">{iconMap[cat.name] || <Users size={20} />}</span>
                  {cat.name}
                </div>
              ))}
            </div>
          ) : (
          // ... (Previous logic same rahega)
    <div className="members-section">
      {/* 1. Back Button Sabse Upar */}
      <button className="back-btn-top" onClick={() => setSelectedCategory(null)}>
        <ChevronLeft size={16} /> Back to Categories
      </button>
    <div className="members-flex-container">
      {members.length > 0 ? members.map((m, idx) => (
        <div key={idx} className="alumni-card-custom">
          <div className="alumni-photo-wrapper">
            <img 
              src={getImageUrl(m.photo)} 
              alt={m.name} 
              className="alumni-photo-img" 
            />
          </div>
          <div className="alumni-details">
            <h3 className="alumni-name">{m.name}</h3>
            <span className="alumni-position">{m.position}</span>
            <div className="alumni-meta">
              Batch {m.batch}
            </div>
            <div className="alumni-meta">
              {m.course}
            </div>
          </div>
        </div>
      )) : (
        <div className="no-data-premium">Records are being updated...</div>
      )}
    </div>
  </div>
          )}
        </div></div>
      <Footer />
    </>
  );
}