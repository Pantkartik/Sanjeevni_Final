import React from "react";

export default function Hero() {
  return (
    <section
      style={{
        marginTop: 110,
        textAlign: "center",
        padding: "64px 18px 0 18px",
        maxWidth: 840,
        marginLeft: "auto",
        marginRight: "auto",
      }}
    >
      <div
        style={{
          display: "inline-block",
          backgroundColor: "#22C55E",
          color: "#fff",
          fontWeight: "600",
          fontSize: 14,
          padding: "6px 18px",
          borderRadius: 8,
          marginBottom: 24,
          userSelect: "none",
        }}
      >
        AI-Powered Healthcare Platform
      </div>
      <h1
        style={{
          fontWeight: 800,
          fontSize: "3.5rem",
          lineHeight: 1.1,
          marginBottom: 24,
          userSelect: "none",
        }}
      >
        Your Complete Health <br /> Companion
      </h1>
      <p
        style={{
          color: "#4B5563",
          fontSize: "1.15rem",
          maxWidth: 600,
          margin: "0 auto 48px auto",
          userSelect: "none",
          lineHeight: 1.35,
        }}
      >
        Sanjeevni combines AI-powered health predictions, smart pill reminders,
        mental health tracking, <br /> and teleconsultation in one comprehensive
        platform designed for the Indian healthcare ecosystem.
      </p>
      <div style={{ display: "inline-flex", gap: 16 }}>
        <button
          type="button"
          style={{
            backgroundColor: "#15803D",
            border: "none",
            color: "white",
            fontWeight: "700",
            padding: "12px 38px",
            borderRadius: 48,
            cursor: "pointer",
            fontSize: "1.125rem",
            boxShadow: "0px 8px 24px rgba(22, 163, 74, 0.48)",
            userSelect: "none",
          }}
        >
          Get Started Free
        </button>
        <button
          type="button"
          style={{
            backgroundColor: "transparent",
            border: "1.9px solid #D1D5DB",
            color: "#111827",
            fontWeight: "600",
            padding: "12px 30px",
            borderRadius: 48,
            cursor: "pointer",
            fontSize: "1.125rem",
            userSelect: "none",
          }}
        >
          ▶ Watch Demo
        </button>
      </div>
    </section>
  );
}
