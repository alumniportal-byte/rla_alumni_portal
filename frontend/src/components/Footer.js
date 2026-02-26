"use client";
import Link from "next/link";
import SubFooter from "../components/SubFooter";

export default function Footer({ registerLink = "#" }) {
  return (
    <>
    <footer>
      <div className="footer-content">
        <div className="footer-section">
          <h3>Contact Us</h3>
          <p><strong>Ram Lal Anand College</strong></p>
          <p>5, Benito Juarez Road, South Campus, New Delhi - 110021</p>
          <p>📞 +91-9217619902</p>
          <Link href="mailto:rlaalumni@rla.du.ac.in" style={{ color: "white" }}>📧 rlaalumni@rla.du.ac.in</Link>
        </div>

        <div className="footer-section">
          <h3>Location</h3>
          <div style={{ marginTop: '15px', borderRadius: '10px', overflow: 'hidden' }}>
            <iframe
              width="100%"
              height="100"
              frameBorder="0"
              style={{ border: 0 }}
              src={process.env.NEXT_PUBLIC_GOOGLE_MAPS_EMBED_URL}
              allowFullScreen
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
              title="map"
            ></iframe>
          </div>
        </div>

        <div className="footer-section">
          <h3>Quick Links</h3>
          <ul style={{ listStyle: "none", lineHeight: 2, color: "white" }}>
            <li><Link href={registerLink} style={{ color: "white" }} target="_blank">Register</Link></li>
            <li><Link href="https://forms.gle/xYHE5HMMwqEz9vFH7" style={{ color: "white" }} target="_blank">Donate</Link></li>
            <li><Link href="#" style={{ color: "white" }} target="_blank">Notices</Link></li>
          </ul>
        </div>

        <div className="footer-section">
          <h3>Follow Us</h3>
          <div className="social-icons">
            <Link href={process.env.NEXT_PUBLIC_SOCIAL_FACEBOOK} target="_blank"><i className="fab fa-facebook"></i></Link>
            <Link href={process.env.NEXT_PUBLIC_SOCIAL_LINKEDIN} target="_blank"><i className="fab fa-linkedin"></i></Link>
            <Link href={process.env.NEXT_PUBLIC_SOCIAL_TWITTER} target="_blank"><i className="fab fa-x-twitter"></i></Link>
            <Link href={process.env.NEXT_PUBLIC_SOCIAL_INSTAGRAM} target="_blank"><i className="fab fa-instagram"></i></Link>
          </div>
        </div>
      </div>
    </footer>
    <SubFooter/>
    </>
  );
}