import React from "react";

export default function DoctorDetails() {
  return (
    <div style={{ marginLeft: 240, padding: "32px", maxWidth: 1200, fontFamily: "'Inter', sans-serif" }}>
      <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 24 }}>Doctor Profile</h1>
      <div style={{ display: "flex", gap: 32 }}>
        <div style={{ flexShrink: 0 }}>
          <img
            src="https://randomuser.me/api/portraits/women/68.jpg"
            alt="Dr. Sneha Patel"
            style={{ width: 160, height: 160, borderRadius: "50%", objectFit: "cover" }}
          />
        </div>
        <div>
          <h2 style={{ marginTop: 0 }}>Dr. Sneha Patel</h2>
          <p style={{ fontSize: 18, color: "#16A34A", fontWeight: 700 }}>Cardiologist</p>
          <p>Delhi, India</p>
          <div style={{ margin: "12px 0" }}>
            <strong>Experience:</strong> 17 years
          </div>
          <div>
            <strong>Languages:</strong> English, Hindi, Marathi
          </div>
          <div style={{ margin: "24px 0" }}>
            <button
              style={{
                backgroundColor: "#15803D",
                color: "white",
                border: "none",
                borderRadius: 8,
                padding: "12px 24px",
                fontWeight: 700,
                cursor: "pointer",
              }}
              onClick={() => alert("Booking appointment with Dr. Sneha Patel")}
            >
              Book Appointment
            </button>
            <button
              style={{
                backgroundColor: "#fff",
                color: "#15803D",
                border: "2px solid #15803D",
                borderRadius: 8,
                padding: "12px 24px",
                fontWeight: 700,
                marginLeft: 12,
                cursor: "pointer",
              }}
              onClick={() => alert("Message Dr. Sneha Patel")}
            >
              Message
            </button>
          </div>
          <div>
            <h3>About</h3>
            <p>
              Dr. Sneha Patel is a leading cardiologist with expertise in advanced heart failure treatments and preventive cardiac care. She has helped numerous patients improve their heart health through comprehensive care plans.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
