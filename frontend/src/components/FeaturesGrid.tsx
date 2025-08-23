import React from "react";

const features = [
  {
    icon: (
      <svg width="20" height="20" fill="#047857" viewBox="0 0 24 24" stroke="none">
        <rect x="4" y="4" width="16" height="16" rx="2" fill="#DCFCE7" />
        <path d="M9 11h6m-3-3v6" stroke="#065F46" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    title: "Smart Pill Reminders",
    description:
      "Never miss a dose with AI-powered notifications, voice alerts, and caregiver notifications",
  },
  {
    icon: (
      <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="#047857">
        <rect x="4" y="4" width="16" height="16" rx="2" fill="#DCFCE7" />
        <path d="M14 11v6m-4-6v6" stroke="#065F46" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    title: "AI Health Predictions",
    description:
      "Upload medical images for AI analysis of skin conditions, chest X-rays, and eye scans",
  },
  {
    icon: (
      <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="#047857">
        <rect x="4" y="4" width="16" height="16" rx="2" fill="#DCFCE7" />
        <path d="M12 7v10M7 12h10" stroke="#065F46" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    title: "Mental Health Tracker",
    description:
      "AI-powered mood analysis with CBT-based exercises and daily wellness tracking",
  },
  {
    icon: (
      <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="#047857">
        <rect x="4" y="4" width="16" height="16" rx="2" fill="#DCFCE7" />
        <path d="M12 14v-4m2 0H10" stroke="#065F46" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    title: "Doctor Integration",
    description:
      "Seamless teleconsultation with secure health record sharing and appointment booking",
  },
  {
    icon: (
      <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="#047857">
        <rect x="4" y="4" width="16" height="16" rx="2" fill="#DCFCE7" />
        <circle cx="12" cy="12" r="3" stroke="#065F46" strokeWidth="2" />
      </svg>
    ),
    title: "Health Dashboard",
    description:
      "Comprehensive view of your health metrics, trends, and personalized insights",
  },
  {
    icon: (
      <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="#047857">
        <rect x="4" y="4" width="16" height="16" rx="2" fill="#DCFCE7" />
        <path d="M17 9l-5 5-3-3" stroke="#065F46" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    title: "Community Support",
    description:
      "Connect with peers, join support groups, and access verified health information",
  },
];

export default function FeaturesGrid() {
  return (
    <section
      id="features"
      style={{
        margin: "80px auto 0 auto",
        maxWidth: 1200,
        padding: "0 18px",
      }}
    >
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
          gap: 32,
        }}
      >
        {features.map((feature) => (
          <div
            key={feature.title}
            style={{
              padding: 32,
              borderRadius: 18,
              boxShadow: "0 6px 18px rgba(0,0,0,.06)",
              backgroundColor: "#F9FAFB",
              minHeight: 160,
            }}
          >
            <div
              style={{
                backgroundColor: "#DCFCE7",
                width: 48,
                height: 48,
                borderRadius: "50%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginBottom: 24,
                color: "#047857",
              }}
            >
              {feature.icon}
            </div>
            <h3 style={{ fontWeight: 700, fontSize: 20, marginBottom: 8 }}>{feature.title}</h3>
            <p style={{ fontWeight: 400, fontSize: 16, color: "#374151", margin: 0 }}>
              {feature.description}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
