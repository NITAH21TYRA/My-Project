import React from 'react';
import './footer.css'; // Create a CSS file for styling
import tiktokIcon from './tictok-removebg-preview.png'; // Adjust the path as needed
import instagramIcon from './instagram-removebg-preview.png'; // Adjust the path as needed
import whatsappIcon from './whatsapp-removebg-preview.png'; // Adjust the path as needed

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p>© 2024 Fierce Jewelry & Accessories. All rights reserved.</p>
        <div className="social-media">
          <a href="https://www.tiktok.com/@fierce_256" target="_blank" rel="noopener noreferrer">
            <img src={tiktokIcon} alt="TikTok" className="footer-icon-img" /> 
          </a>
          <a href="https://www.instagram.com/fierce_256" target="_blank" rel="noopener noreferrer">
            <img src={instagramIcon} alt="Instagram" className="footer-icon-img" />
          </a>
          <a href="https://wa.me/256753031602" target="_blank" rel="noopener noreferrer">
            <img src={whatsappIcon} alt="WhatsApp" className="footer-icon-img" />
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
