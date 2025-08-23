// App.tsx
import React, { useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Header from "./components/Header";
import AuthModal from "./components/AuthModal";
import Hero from "./components/Hero";
import FeaturesGrid from "./components/FeaturesGrid";
import Testimonials from "./components/Testimonials";
import Footer from "./components/Footer";
import Sidebar from "./components/Sidebar";
import Dashboard from "./components/Dashboard";
import Community from "./components/Community";
import AppointmentManagement from "./components/AppointmentManagement";
// import PillReminders from "./components/PillReminders";
// import MentalHealthTracking from "./components/MentalHealthTracking";
// import Teleconsultation from "./components/Teleconsultation";
// import HealthPredictions from "./components/HealthPredictions";
// import HealthAnalysis from "./components/HealthAnalysis";
// import Doctors from "./components/Doctors";
// import AnalysisDetails from "./components/AnalysisDetails";
// import PatientProfile from "./components/PatientProfile";

export default function App() {
  const [authOpen, setAuthOpen] = useState<null | "signup" | "login">(null);
  const [loggedIn, setLoggedIn] = useState(false);

  function handleLoginSuccess() {
    setLoggedIn(true);
    setAuthOpen(null);
  }

  if (!loggedIn) {
    return (
      <>
        <Header onOpenAuth={mode => setAuthOpen(mode)} />
        <main>
          <Hero />
          <FeaturesGrid />
          <Testimonials />
          <AuthModal
            open={authOpen !== null}
            mode={authOpen ?? "login"}
            onClose={() => setAuthOpen(null)}
            switchMode={mode => setAuthOpen(mode)}
            onLoginSuccess={handleLoginSuccess}
          />
        </main>
        <Footer />
      </>
    );
  }

  return (
    <>
      <Header onOpenAuth={mode => setAuthOpen(mode)} />
      <div style={{ display: "flex" }}>
        <Sidebar />
        <main style={{ flexGrow: 1, padding: 20 }}>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/community" element={<Community />} />
            {/* <Route path="/appointment-management" element={<AppointmentManagement />} />
            <Route path="/pill-reminders" element={<PillReminders />} />
            <Route path="/mental-health-tracking" element={<MentalHealthTracking />} />
            <Route path="/teleconsultation" element={<Teleconsultation />} />
            <Route path="/health-predictions" element={<HealthPredictions />} />
            <Route path="/health-analysis" element={<HealthAnalysis />} />
            <Route path="/doctors" element={<Doctors />} />
            <Route path="/analysis-details" element={<AnalysisDetails />} />
            <Route path="/profile" element={<PatientProfile />} /> */}
          </Routes>
        </main>
      </div>
    </>  
  );
}
