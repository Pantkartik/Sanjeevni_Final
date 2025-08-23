// Sidebar.tsx
import React from "react";
import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <nav style={{ width: 200, background: "#eee", padding: 20 }}>
      <ul style={{ listStyle: "none", padding: 0 }}>
        <li><NavLink to="/dashboard">Dashboard</NavLink></li>
        <li><NavLink to="/community">Community</NavLink></li>
        <li><NavLink to="/appointment-management">Appointments</NavLink></li>
        <li><NavLink to="/pill-reminders">Pill Reminders</NavLink></li>
        <li><NavLink to="/mental-health-tracking">Mental Health</NavLink></li>
        <li><NavLink to="/teleconsultation">Teleconsultation</NavLink></li>
        <li><NavLink to="/health-predictions">Health Predictions</NavLink></li>
        <li><NavLink to="/health-analysis">Health Analysis</NavLink></li>
        <li><NavLink to="/doctors">Doctors</NavLink></li>
        <li><NavLink to="/analysis-details">Analysis Details</NavLink></li>
      </ul>
    </nav>
  );
}
