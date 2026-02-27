"use client";
import { useSearchParams } from "next/navigation";
import { useEffect, useState,Suspense } from "react";

import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import link from "next/link";

// --- STEP 1: GLOBAL CONSTANTS (Exports ke bahar) ---
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

// --- STEP 2: HELPER FUNCTION (Top level par) ---

// --- STEP 3: MAIN COMPONENT ---
function AboutContent() {
  const searchParams = useSearchParams();
  const tab = searchParams.get("tab") || "college"; 

  // Dynamic Title Logic
  const getHeroTitle = () => {
    const titles = {
      patron: "Patron's Message",
      college: "History & Heritage",
      heritage: "History & Heritage",
      faculty: "Teaching Faculty",
      staff: "Non-Teaching Staff",
      association: "About Alumni Association",
      bearers: "Association Office Bearers",
      committee: "College Alumni Committee",
      preamble: "Preamble & Documents"
    };
    return titles[tab] || "About Our Institution";
  };

  return (
    <>
      <Navbar />
      <div className="about-page-wrapper">
         <header className="about-hero">
            <h1 className="hero-title">{getHeroTitle()}</h1>
            <div className="gold-accent-line"></div>
         </header>  

         <div className="about-tab-content-wrapper">
            {/* Existing Tabs */}
            {(tab === "college" || tab === "heritage") && <AboutCollege />}
            {tab === "patron" && <PatronMessage />}
            {tab === "association" && <Association />}
            {tab === "bearers" && <AlumniAssociationOfficeBearers apiBase={API_BASE_URL} />}
            {tab === "committee" && <Committee apiBase={API_BASE_URL} />}
            {tab === "preamble" && <Preamble />}

            {/* New Tabs (Inka component hum next step mein banayenge) */}
            {tab === "faculty" && <TeachingFaculty apiBase={API_BASE_URL} />}
            {tab === "staff" && <NonTeachingStaff apiBase={API_BASE_URL} />}
         </div>
      </div>
      <Footer />
    </>
  );
}
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
// ============================================
// 2.1 ABOUT COLLEGE COMPONENT
// ============================================
function AboutCollege() {
  return (
    <div className="about-main-container">
      
      {/* --- TITLE SECTION --- */}
      <div className="section-header">
      </div>

      {/* --- MAIN CARD (White Box with Shadow) --- */}
      <div className="unified-card-wrap">
        
        {/* --- IMAGE SECTION (Floated Left) --- */}
        <div className="founder-image-box">
          <div className="img-frame">
            <img 
              src="/images/Founder.jpg" 
              alt="RLA College Founder" 
              className="founder-img-rect" 
            />
          </div>
          <div className="img-caption">
            <strong>Late Sh. Ram Lal Anand</strong>
            <br/>Founder (1895-1966)
          </div>
        </div>

        {/* --- TEXT CONTENT --- */}
        <div className="text-content-wrap">
          <p>
            Ram Lal Anand College was founded in the year 1964 by <strong>Late Shri Ram Lal Anand</strong>, a senior advocate in the Supreme Court of India, in response to the growing social demand in the sixties for providing educational opportunities at the university level. The college was initially managed by the Ram Lal Anand College Trust. It was later taken over by the University of Delhi. Since 1973, it has been run by the University of Delhi as a University Maintained Institution.
          </p>
          <p>
            The college is located in the picturesque surroundings against the backdrop of the Aravali ranges in the neighbourhood of the South Campus of the University of Delhi and several other educational institutions. It has a vast campus, spread over ten acres of land with green lawns and elegant buildings of much sprawling architectural merit. The college has excellent infrastructure, with state of the art Laboratories, Seminar room, Amphitheatre, Library, Playground and Cafeteria.
          </p>
          <p>
            The campus is Wi-Fi enabled. Being a multi-disciplinary, co-educational institution it has approximately 2520 students pursuing different courses in Arts, Commerce and Science streams. Ram Lal Anand College is administered by a statutory Governing Body as per the University Ordinances and legislated by the Executive Council of the University of Delhi.
          </p>
          <p>
            The college boasts off a highly learned and committed teaching faculty of about 80 teachers. Apart from their traditional role of disseminating knowledge, the teachers inspire and guide the students to manage different activities such as seminars, workshops, debates, theatre, cultural activities including classical music and dance programmes. Teachers are also involved in guiding students in various research and innovation projects.
          </p>
        </div>
        
        {/* Clearfix (Zaroori hai taaki card image ko cover kare) */}
        <div style={{ clear: "both" }}></div>
      </div>

      {/* --- VIDEO SECTION --- */}
      <div className="video-section-container">
        <h3 className="sub-title">Campus Glimpses</h3>
        <div className="video-grid">
          <div className="video-card">
            <iframe src="https://www.youtube.com/embed/yfwcFoddMTs" title="Campus Tour" allowFullScreen></iframe>
          </div>
          <div className="video-card">
            <iframe src="https://www.youtube.com/embed/HZnKXxuDkAc" title="College Event" allowFullScreen></iframe>
          </div>
        </div>
      </div>

    </div>
  );
}
// ============================================
// 2.2 PATRON'S MESSAGE
// ============================================
function PatronMessage() {
  const [isExpanded, setIsExpanded] = useState(false);

  // Full content ko paragraphs mein divide kiya hai
  const paragraphs = [
    "Ramlal Anand College welcomes you all. When Ramlal Anand College was established, its objective was to prepare the youth of emerging India for nation-building through higher education. I am pleased that the college has succeeded in achieving its goals and endeavors since its inception. Our students are achieving excellence in diverse fields of politics, education, industry, business, and research.",
    "Today, due to information technology and globalization, the challenges facing youth have increased significantly, but I am pleased to report that Ramlal Anand College is fully prepared for this national challenge. We have made efforts to continuously enhance the college's infrastructure, evidenced by a fully air-conditioned, information technology-enabled, well-stocked library, labs, classrooms, and studios equipped with modern facilities and equipment.",
    "A scholar once said that if a country's progress is to be measured, it should be measured by the progress of its women. That is why we have declared women's day as a national holiday. We have a strong commitment to women's empowerment as our goal. We are pursuing this through education and knowledge, embracing the ideals of equality, self-reliance, and independence.",
    "Driven by the goals of rationality, scientific consciousness, social harmony, and environmental protection, all the faculty at the college prepare students for future challenges and present responsibilities.",
    "At Ramlal Anand College, you will all be provided with an environment where students can continuously improve themselves. I hope that in these three years of higher education, you will complete a journey of talent, knowledge, discipline, experimentation, and innovation that will take your lives to the pinnacle of success and meaning."
  ];

  const toggleReadMore = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="patron-wrapper">
      <div className="section-header" style={{textAlign: 'center', marginBottom: '30px'}}>
    </div>

      <div className="patron-card">
        {/* --- Left Side: Photo & Designation --- */}
        <div className="patron-profile">
          <div className="profile-img-container">
            <img 
              src="/images/principal.jpg" 
              alt="Principal Prof. Rakesh Kumar Gupta" 
              className="patron-img" 
            />
          </div>
          <div className="patron-name-plate">
            <h3>Prof. Rakesh Kumar Gupta</h3>
            <p>Principal</p>
            <span className="college-name">Ram Lal Anand College</span>
          </div>
        </div>

        {/* --- Right Side: Message Content --- */}
        <div className="patron-content">
          <div className="quote-icon">❝</div>
          
          <div className={`message-text ${!isExpanded ? 'clamped' : ''}`}>
            {/* Pehla paragraph hamesha dikhega */}
            <p>{paragraphs[0]}</p>
            <p>{paragraphs[1]}</p>
  
            {/* Baki paragraphs toggle honge */}
            {isExpanded && (
              <div className="expanded-content animate-fadeIn">
                {paragraphs.slice(1).map((p, index) => (
                  <p key={index}>{p}</p>
                ))}
              </div>
            )}
          </div>

          <button onClick={toggleReadMore} className="read-more-btn">
            {isExpanded ? "Read Less ▲" : "Read More ▼"}
          </button>

          <div className="patron-sign">
            <p>Best Wishes,</p>
            <strong>Principal</strong>
          </div>
        </div>
      </div>
    </div>
  );
}
function TeachingFaculty({ apiBase }) {
  const [departments, setDepartments] = useState([]);
  const [openDeptId, setOpenDeptId] = useState(null); // Accordion toggle state
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${apiBase}/api/faculty/`)
      .then(res => res.json())
      .then(data => {
        setDepartments(data);
        setLoading(false);
      });
  }, [apiBase]);

  const toggleDept = (id) => {
    setOpenDeptId(openDeptId === id ? null : id);
  };

  if (loading) return <div className="loader-simple">Loading Faculty...</div>;

  return (
    <div className="faculty-accordion-container">
      <div className="section-header">
          <h2 className="section-title">List of Departments</h2>
      </div>

      <div className="accordion-list">
        {departments.map((dept) => (
          <div key={dept.id} className={`accordion-item ${openDeptId === dept.id ? 'active' : ''}`}>
            {/* Header: Department Name */}
            <div className="accordion-header" onClick={() => toggleDept(dept.id)}>
              <div className="dept-info">
                <span className="dept-icon">📖</span>
                <h3 className="dept-title-text">{dept.name}</h3>
              </div>
              <div className="dept-action">
                <span className="faculty-count">{dept.teachers.length} Faculty Members</span>
                <span className="arrow-icon">{openDeptId === dept.id ? '▲' : '▼'}</span>
              </div>
            </div>

            {/* Content: Teachers List (Animated) */}
            <div className="accordion-content">
              <div className="teachers-list-wrapper">
                {dept.teachers.map((t, idx) => (
                  <div key={idx} className="faculty-row-item">
                    <div className="faculty-avatar">
                      <img src={getImageUrl(t.image)} alt={t.name} />
                    </div>
                    <div className="faculty-main-details">
                      <h4 className="faculty-name-text">{t.name}</h4>
                      <p className="faculty-desig-text">{t.designation}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function NonTeachingStaff({ apiBase }) {
  const [sections, setSections] = useState([]);
  const [openSectionId, setOpenSectionId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${apiBase}/api/staff/`)
      .then(res => res.json())
      .then(data => {
        setSections(data);
        setLoading(false);
      });
  }, [apiBase]);

  if (loading) return <div className="loader-simple">Loading Staff...</div>;

  return (
    <div className="faculty-accordion-container">
      <div className="accordion-list">
        {sections.map((section, sIdx) => (
          <div key={sIdx} className={`accordion-item ${openSectionId === sIdx ? 'active' : ''}`}>
            
            {/* Accordion Header (Section Name) */}
            <div className="accordion-header staff-header" onClick={() => setOpenSectionId(openSectionId === sIdx ? null : sIdx)}>
              <div className="dept-info">
                <span className="dept-icon">💼</span>
                <h3 className="dept-title-text">{section.name}</h3> {/* Yahan "Accounts Section" aayega */}
              </div>
              <div className="dept-action">
                <span className="faculty-count staff-count">
                  {section.staff_members?.length || 0} Members
                </span>
                <span className="arrow-icon">{openSectionId === sIdx ? '▲' : '▼'}</span>
              </div>
            </div>

            {/* Accordion Content (Members Table) */}
            <div className="accordion-content">
              <div className="staff-table-inside">
                <table className="mini-staff-table">
                  <thead>
                    <tr>
                      <th>S.No</th>
                      <th>Name</th>
                      <th>Designation</th>
                    </tr>
                  </thead>
                  <tbody>
                    {section.staff_members?.map((s, mIdx) => (
                      <tr key={mIdx}>
                        <td>{mIdx + 1}</td>
                        <td className="staff-name-cell">{s.name}</td>
                        <td><span className="staff-badge">{s.designation}</span></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        ))}
      </div>
    </div>
  );
}
// ============================================
// 2.3 ALUMNI ASSOCIATION (Static)
// ============================================
function Association() {
  return (
    <div className="association-container">
      
      {/* --- HEADER --- */}
      <div className="section-header">
      </div>

      <div className="association-content">
        {/* --- OBJECTIVE SECTION (Blue Theme) --- */}
      <div className="info-box objective-box">
          <h3 className="box-title">Our Vision</h3>
          <p> The Ram Lal Anand College Alumni Association was established to To build a vibrant, inclusive, and lifelong alumni community that actively contributes to the academic excellence, social impact, and holistic development of Ram Lal Anand College, while fostering strong connections among alumni, students, and the institution at a global level.
       </p>
        </div>

        {/* --- MISSION SECTION (Red Theme) --- */}
        <div className="info-box mission-box">
          <h3 className="box-title">Our Mission</h3>
          <ul className="custom-list">
            <li>To connect alumni across generations, disciplines, and geographies through a strong and engaged alumni network.</li>
            <li>To promote mentorship, collaboration, and knowledge exchange between alumni and current students.</li>
            <li>To support the academic growth and career development of students through guidance, internships, and scholarships.</li>
            <li>To celebrate and showcase the achievements, contributions, and legacy of the College and its alumni.</li>
            <li>To encourage alumni participation in institutional development, innovation, and social responsibility initiatives</li>
            <li>To mobilize resources and partnerships to strengthen alumni-led programs and initiatives.</li>
          </ul>
        </div>

        {/* --- OBJECTIVES SECTION (Gold Theme) --- */}
        <div className="info-box objective-box">
          <h3 className="box-title">Our Objectives</h3>
          <ul className="custom-list">
            <li>To foster lifelong connections among alumni, students, and the College community.</li>
            <li>To build a strong national and global alumni network for mutual support and engagement.</li>
            <li>To promote professional, academic, and socio-cultural interaction among alumni.</li>
            <li>To encourage alumni participation in the growth and development of the College.</li>
            <li>To facilitate mentorship, knowledge sharing, and collaboration between alumni and current students.</li>
            <li>To recognize and promote the achievements and legacy of the College and its alumni.</li>
            <li>To organize lectures, workshops, and events that support learning and dialogue.</li>
            <li>To support deserving students through scholarships, bursaries, and educational assistance.</li>
            <li>To undertake civic, charitable, and socially responsible initiatives aligned with the Association&apos;s mission.</li>
            <li>To mobilize resources and partnerships to strengthen alumni-driven initiatives.</li>
          </ul>
        </div>

      </div>
    </div>
  );
}
// ============================================
// 2.4 OFFICE BEARERS (Dynamic from API)
// ============================================
function AlumniAssociationOfficeBearers({ apiBase }) {
  const [bearers, setBearers] = useState([]);

  useEffect(() => {
    fetch(`${apiBase}/api/bearers/`)
      .then(res => res.json())
      .then(data => setBearers(Array.isArray(data) ? data : []))
      .catch(err => console.error(err));
  }, [apiBase]);

  return (
    <div className="bearers-container">
      <div className="bearers-list">
        {bearers.map((b) => (
          <div key={b.id} className="bearer-card">
            
            {/* Round Image Container */}
            <div className="bearer-img-container">
              <img 
                src={getImageUrl(b.image)} 
                alt={b.name} 
                className="bearer-full-img" 
              />
            </div>

            {/* Content Section */}
            <div className="bearer-content">
              <div className="bearer-header">
                <h3 className="bearer-name">{b.name}</h3>
                <span className="bearer-badge">{b.position}</span>
              </div>
              
              <div className="bearer-body">
                <p>
                  <span className="quote-mark">“</span>
                  {b.message}
                </p>
              </div>
            </div>

          </div>
        ))}
      </div>
    </div>
  );
}
// ============================================
// 2.5 COLLEGE COMMITTEE (Year Wise)
// ============================================
function Committee({ apiBase }) {
  const [years, setYears] = useState([]);
  const [selectedYear, setSelectedYear] = useState(null);

  useEffect(() => {
    fetch(`${apiBase}/api/committee/`)
      .then(res => res.json())
      .then(data => {
        setYears(data);
        if(data.length > 0) setSelectedYear(data[0]); // Auto select latest
      })
      .catch(err => console.error(err));
  }, [apiBase]);

  return (
    <div className="committee-container">
      
      {/* Year Selection (Tabs Style) */}
      <div className="year-tabs">
        {years.map((y) => (
          <button 
            key={y.id} 
            className={`year-tab-btn ${selectedYear?.id === y.id ? 'active' : ''}`}
            onClick={() => setSelectedYear(y)}
          >
            {y.session}
          </button>
        ))}
      </div>

      {/* Members Table */}
      {selectedYear && (
        <div className="table-container fade-in">
          <div className="table-header-strip">
             <h3>Committee Members ({selectedYear.session})</h3>
          </div>
          <table className="custom-table">
            <thead>
              <tr>
                <th style={{width: '80px'}}>S.No.</th>
                <th>Role</th>
                <th>Name</th>
              </tr>
            </thead>
            <tbody>
              {selectedYear.members.map((m, index) => (
                <tr key={m.id}>
                  {/* S.No. logic: index starts from 0, so +1 */}
                  <td>{index + 1}</td>
                  <td className="role-cell">{m.role}</td>
                  <td className="name-cell">{m.name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

// ============================================
// 2.6 PREAMBLE (Docs)
// ============================================
import React from 'react';

export function Preamble() {
  const documents = [
    { 
      id: 1, 
      title: "Constitution", 
      sub: "Rules & Regulations",
      file: "/docs/constitution.pdf" 
    },
    { 
      id: 2, 
      title: "Memorandum of Association", 
      sub: "Objectives & Scope", 
      file: "/docs/moa.pdf" 
    }
  ];

  return (
    <div className="preamble-section">

      <div className="docs-grid">
        {documents.map((doc) => (
          <div key={doc.id} className="doc-card">
            <a href={doc.file} target="_blank" rel="noopener noreferrer" className="doc-link">
              
              {/* --- DOCUMENT COVER --- */}
              <div className="doc-cover">
                {/* Binding Spine (Book jaisa look) */}
                <div className="doc-spine"></div>

                <div className="doc-content-wrapper">
                  <div className="doc-header">
                     <span className="college-name">RLAC ALUMNI</span>
                     <div className="doc-logo-circle">⚖️</div>
                  </div>
                  
                  <h3 className="doc-cover-title">{doc.title}</h3>
                  <div className="doc-divider"></div>
                  <p className="doc-cover-sub">{doc.sub}</p>
                  
                  <div className="doc-footer-decor">
                    <div className="seal-mark">OFFICIAL<br/>RECORD</div>
                  </div>
                </div>

                {/* Hover Overlay */}
                <div className="doc-overlay">
                  <span className="view-btn">📄 Open PDF</span>
                </div>
              </div>
              
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}
export default function AboutPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <AboutContent />
    </Suspense>
  );
}
