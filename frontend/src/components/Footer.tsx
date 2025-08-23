import React from "react";

export default function Footer() {
  return (
    <footer
      style={{
        padding: "38px 0 18px 0",
        background: "#F9FAFB",
        borderTop: "1.5px solid #E5E7EB",
        marginTop: 110,
      }}
    >
      <div
        style={{
          maxWidth: 1200,
          margin: "0 auto 10px",
          padding: "0 18px",
          display: "flex",
          justifyContent: "space-between",
          flexWrap: "wrap",
          gap: 40,
          color: "#374151",
        }}
      >
        <div style={{ maxWidth: 280 }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 11,
              marginBottom: 12,
              color: "#064E3B",
              fontWeight: 700,
              fontSize: 20,
            }}
          >
            <div
              style={{
                backgroundColor: "#22C55E",
                padding: 6,
                borderRadius: 8,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                width: 40,
                height: 40,
              }}
            >
              <svg
                width="24"
                height="24"
                fill="white"
                viewBox="0 0 20 20"
                aria-hidden="true"
              >
                <path d="M10 17s6.875-4.625 7.875-8C18.875 5.625 15.375 3 10 8.125C4.625 3 1.125 5.625 2.125 9C3.125 12.375 10 17 10 17z" />
              </svg>
            </div>
            Sanjeevni
          </div>
          <div style={{ fontSize: 15, lineHeight: 1.6 }}>
            AI-powered healthcare platform for comprehensive health management
          </div>
        </div>

        <div>
          <div style={{ fontWeight: 600, marginBottom: 10, fontSize: 16 }}>
            Features
          </div>
          <ul style={{ listStyle: "none", padding: 0, fontSize: 15 }}>
            <li>Pill Reminders</li>
            <li>Health Predictions</li>
            <li>Mental Health</li>
            <li>Teleconsultation</li>
          </ul>
        </div>

        <div>
          <div style={{ fontWeight: 600, marginBottom: 10, fontSize: 16 }}>
            Support
          </div>
          <ul style={{ listStyle: "none", padding: 0, fontSize: 15 }}>
            <li>Help Center</li>
            <li>Contact Us</li>
            <li>Privacy Policy</li>
            <li>Terms of Service</li>
          </ul>
        </div>

        <div>
          <div style={{ fontWeight: 600, marginBottom: 10, fontSize: 16 }}>
            Company
          </div>
          <ul style={{ listStyle: "none", padding: 0, fontSize: 15 }}>
            <li>About Us</li>
            <li>Careers</li>
            <li>Blog</li>
            <li>Press</li>
          </ul>
        </div>
      </div>
      <div
        style={{
          textAlign: "center",
          color: "#374151",
          fontSize: 13,
          marginTop: 12,
          userSelect: "none",
        }}
      >
        &copy; 2024 Sanjeevni. All rights reserved.
      </div>
    </footer>
  );
}
