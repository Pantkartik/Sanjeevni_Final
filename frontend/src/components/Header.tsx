import React from "react";

interface HeaderProps {
  onOpenAuth: (mode: "login" | "signup") => void;
}

export default function Header({ onOpenAuth }: HeaderProps) {
  return (
    <header className="fixed-header">
      {/* Medical disclaimer banner */}
      <div
        style={{
          backgroundColor: "#FEF3C7",
          color: "#92400E",
          fontSize: 14,
          padding: "4px 0",
          textAlign: "center",
          userSelect: "none",
          position: "fixed",
          width: "100%",
          top: 0,
          zIndex: 1031,
          borderBottom: "1px solid #FBBF24",
        }}
      >
        ⚠ <strong>Medical Disclaimer:</strong> This is a prototype platform. Always consult qualified healthcare professionals for medical advice and treatment.
      </div>

      {/* Navbar */}
      <nav
        className="navbar navbar-expand-lg navbar-light bg-white shadow-sm"
        style={{
          position: "fixed",
          width: "100%",
          top: 32,
          zIndex: 1030,
          paddingLeft: "1rem",
          paddingRight: "1rem",
        }}
      >
        <div className="container d-flex justify-content-between align-items-center">
          {/* Brand/logo */}
          <div className="d-flex align-items-center gap-2 fw-semibold" style={{ fontSize: 24, color: "#064E3B" }}>
            <div
              style={{
                backgroundColor: "#16A34A",
                padding: 6,
                borderRadius: 8,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                width: 32,
                height: 32,
              }}
            >
              <svg width={20} height={20} fill="white" viewBox="0 0 20 20">
                <path d="M10 17s6.875-4.625 7.875-8C18.875 5.625 15.375 3 10 8.125C4.625 3 1.125 5.625 2.125 9C3.125 12.375 10 17 10 17z" />
              </svg>
            </div>
            Sanjeevni
          </div>

          {/* Navigation Links */}
          <ul className="nav d-none d-lg-flex gap-4" style={{ color: "#6B7280", fontSize: 16 }}>
            <li className="nav-item">
              <a className="nav-link" href="#features" style={{ color: "inherit" }}>
                Features
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#testimonials" style={{ color: "inherit" }}>
                Testimonials
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#about" style={{ color: "inherit" }}>
                About
              </a>
            </li>
          </ul>

          {/* Auth Buttons */}
          <div className="d-flex gap-2">
            <button
              type="button"
              className="btn btn-outline-success"
              style={{ borderWidth: 2, fontWeight: 600 }}
              onClick={() => onOpenAuth("login")}
            >
              Login
            </button>
            <button
              type="button"
              className="btn btn-success"
              style={{ fontWeight: 600 }}
              onClick={() => onOpenAuth("signup")}
            >
              Sign Up
            </button>
          </div>
        </div>
      </nav>
    </header>
  );
}
