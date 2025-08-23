import React from "react";

const testimonials = [
  {
    name: "Priya Sharma",
    location: "Mumbai, Maharashtra",
    photo: "https://randomuser.me/api/portraits/women/74.jpg",
    text: "Sanjeevni’s pill reminders have been a game-changer for my elderly mother. The AI predictions caught a skin condition early that we might have missed.",
    rating: 5,
  },
  {
    name: "Rajesh Kumar",
    location: "Bangalore, Karnataka",
    photo: "https://randomuser.me/api/portraits/men/77.jpg",
    text: "The mental health tracking feature helped me understand my stress patterns. The teleconsultation with doctors is seamless and convenient.",
    rating: 5,
  },
  {
    name: "Dr. Sneha Patel",
    location: "Delhi, NCR",
    photo: "https://randomuser.me/api/portraits/women/79.jpg",
    text: "As a doctor, I appreciate how Sanjeevni helps my patients stay compliant with medications and provides valuable health insights between visits.",
    rating: 5,
  },
];

function StarRating({ count }: { count: number }) {
  return (
    <div style={{ color: "#22C55E", fontSize: 18, marginBottom: 12 }}>
      {"★".repeat(count)}
    </div>
  );
}

export default function Testimonials() {
  return (
    <section
      id="testimonials"
      style={{
        margin: "80px auto 100px",
        padding: "0 18px",
        maxWidth: 1200,
        textAlign: "center",
      }}
    >
      <h2 style={{ fontWeight: 700, fontSize: 32, marginBottom: 6 }}>
        Trusted by Thousands
      </h2>
      <p style={{ fontSize: 18, color: "#6B7280", marginBottom: 30 }}>
        See how Sanjeevni is transforming healthcare experiences across India
      </p>
      <div
        style={{
          display: "flex",
          gap: 32,
          justifyContent: "center",
          flexWrap: "wrap",
        }}
      >
        {testimonials.map((t) => (
          <div
            key={t.name}
            style={{
              boxShadow: "0 5px 25px rgba(0,0,0,0.07)",
              borderRadius: 18,
              background: "#fff",
              padding: 30,
              maxWidth: 390,
              flex: "1 1 300px",
              textAlign: "left",
            }}
          >
            <StarRating count={t.rating} />
            <p style={{ fontSize: 16, color: "#3F3F46", marginBottom: 22 }}>
              {t.text}
            </p>
            <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
              <img
                src={t.photo}
                alt={`Photo of ${t.name}`}
                width={44}
                height={44}
                style={{ borderRadius: "50%", objectFit: "cover", border: "2.5px solid #22C55E" }}
              />
              <div>
                <div style={{ fontWeight: 700, fontSize: 16 }}>{t.name}</div>
                <div style={{ color: "#6B7280", fontSize: 14 }}>{t.location}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
