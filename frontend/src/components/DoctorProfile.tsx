import React from "react";

type Doctor = {
  id: number;
  name: string;
  specialty: string;
  rating: number;
  reviews: number;
  experience: number;
  hospital: string;
  location: string;
  languages: string[];
  consultationFee: number;
  nextAvailable: string;
};

const doctors: Doctor[] = [
  {
    id: 1,
    name: "Dr. Sarah Patel",
    specialty: "Cardiologist",
    rating: 4.8,
    reviews: 124,
    experience: 15,
    hospital: "Apollo Hospital",
    location: "Mumbai, Maharashtra",
    languages: ["English", "Hindi"],
    consultationFee: 800,
    nextAvailable: "Today 3:00 PM",
  },
  {
    id: 2,
    name: "Dr. Rajesh Kumar",
    specialty: "Endocrinologist",
    rating: 4.7,
    reviews: 89,
    experience: 12,
    hospital: "Fortis Healthcare",
    location: "Delhi, NCR",
    languages: ["English", "Hindi"],
    consultationFee: 1200,
    nextAvailable: "Tomorrow 10:00 AM",
  },
];

export default function DoctorProfile() {
  return (
    <div style={{ marginLeft: 240, padding: 32, maxWidth: 1200, fontFamily: "'Inter', sans-serif" }}>
      <h1 style={{ fontWeight: 700, fontSize: 28, marginBottom: 24 }}>Find Doctors</h1>

      {doctors.map((doc) => (
        <div
          key={doc.id}
          style={{
            backgroundColor: "#F9FAFB",
            borderRadius: 20,
            padding: 24,
            marginBottom: 24,
            boxShadow: "0 7px 24px rgba(12,41,29,0.05)",
            userSelect: "none",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
            <div>
              <strong>{doc.name}</strong> - <span>{doc.specialty}</span>
              <div style={{ fontSize: 14, color: "#4B5563" }}>{`${doc.rating} stars (${doc.reviews} reviews)`}</div>
            </div>
            <div style={{ fontWeight: 700, fontSize: 20 }}>{`₹${doc.consultationFee}`}</div>
          </div>

          <div style={{ display: "flex", gap: 20, flexWrap: "wrap" }}>
            <div>Hospital: {doc.hospital}</div>
            <div>Location: {doc.location}</div>
            <div>Next Available: {doc.nextAvailable}</div>
            <div>Languages: {doc.languages.join(", ")}</div>
            <div>Experience: {doc.experience} years</div>
          </div>

          <div style={{ marginTop: 12, display: "flex", gap: 12 }}>
            <button
              style={buttonStyle}
              onClick={() => alert(`Booking appointment with ${doc.name}`)}
            >
              Book Appointment
            </button>
            <button style={secondaryButtonStyle} onClick={() => alert(`Video call with ${doc.name}`)}>
              Video Call
            </button>
            <button style={secondaryButtonStyle} onClick={() => alert(`Messaging ${doc.name}`)}>
              Message
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

const buttonStyle: React.CSSProperties = {
  backgroundColor: "#15803D",
  borderRadius: 8,
  color: "#fff",
  fontWeight: 700,
  padding: "10px 28px",
  border: "none",
  cursor: "pointer",
};

const secondaryButtonStyle: React.CSSProperties = {
  backgroundColor: "white",
  borderRadius: 8,
  color: "#374151",
  fontWeight: 700,
  padding: "10px 28px",
  border: "1.5px solid #D1D5DB",
  cursor: "pointer",
};
