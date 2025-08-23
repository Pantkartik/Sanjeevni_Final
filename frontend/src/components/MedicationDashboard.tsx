import React, { useState } from "react";

type Medication = {
  id: number;
  name: string;
  dosage: string;
  schedule: string[];
  notes: string;
  caregiverNotify: boolean;
};

export default function MedicationDashboard() {
  // sample data; you can replace with real data or API integration
  const [medications, setMedications] = useState<Medication[]>([]);

  const [showAddModal, setShowAddModal] = useState(false);

  return (
    <div style={{ marginLeft: 240, padding: "32px 36px", maxWidth: 1200 }}>
      <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 20 }}>
        Pill Reminders
      </h1>

      {/* Summary cards */}
      <div style={{ display: "flex", gap: 16, marginBottom: 24, flexWrap: "wrap" }}>
        <SummaryCard title="Overall Adherence" value="0%" subText="No medications added yet" />
        <SummaryCard title="Active Medications" value={`${medications.length}`} subText="Currently prescribed" />
        <SummaryCard title="Today's Doses" value="0/0" subText="Taken so far" />
        <SummaryCard title="Low Stock Alert" value="0" subText="Needs refill soon" isDanger />
      </div>

      {/* Tabs */}
      <nav style={{ display: "flex", gap: 8, borderBottom: "1px solid #D1D5DB", marginBottom: 24 }}>
        <Tab label="My Medications" active />
        <Tab label="Calendar View" />
        <Tab label="Adherence Report" />
      </nav>

      {/* Content area */}
      <MedicationList medications={medications} onAddClick={() => setShowAddModal(true)} />

      {showAddModal && <AddMedicationModal onClose={() => setShowAddModal(false)} />}
    </div>
  );
}

function SummaryCard({
  title,
  value,
  subText,
  isDanger,
}: {
  title: string;
  value: string;
  subText: string;
  isDanger?: boolean;
}) {
  const progress = value.endsWith("%") ? parseInt(value) : 0;
  const progressColor = isDanger ? "#DC2626" : "#15803D";

  return (
    <div
      style={{
        backgroundColor: "#F9FAFB",
        padding: 24,
        borderRadius: 18,
        flex: "1 1 200px",
        boxShadow: "0 6px 15px rgba(0,0,0,0.06)",
        userSelect: "none",
      }}
    >
      <h3 style={{ fontWeight: 500, fontSize: 16, color: "#52525B" }}>{title}</h3>
      <p style={{ fontWeight: 700, fontSize: 26, margin: "8px 0" }}>{value}</p>
      <p style={{ fontWeight: 500, fontSize: 14, color: isDanger ? "#DC2626" : "#6B7280" }}>{subText}</p>
      {progress > 0 && (
        <div
          style={{
            height: 8,
            borderRadius: 6,
            width: "100%",
            backgroundColor: isDanger ? "#FECACA" : "#D1FAE5",
            marginTop: 8,
          }}
        >
          <div
            style={{
              width: `${progress}%`,
              height: 8,
              borderRadius: 6,
              backgroundColor: progressColor,
              transition: "width 0.3s ease-in-out",
            }}
          />
        </div>
      )}
    </div>
  );
}

function Tab({ label, active }: { label: string; active?: boolean }) {
  return (
    <button
      style={{
        backgroundColor: active ? "#F3F4F6" : "transparent",
        border: "none",
        borderBottom: active ? "3px solid #15803D" : "none",
        borderRadius: 6,
        padding: "8px 20px",
        color: active ? "#15803D" : "#374151",
        fontWeight: active ? 700 : 500,
        cursor: "pointer",
        userSelect: "none",
      }}
    >
      {label}
    </button>
  );
}

function MedicationList({ medications, onAddClick }: { medications: Medication[]; onAddClick: () => void }) {
  return (
    <>
      <button
        style={{
          marginBottom: 24,
          padding: "12px 24px",
          backgroundColor: "#15803D",
          color: "white",
          border: "none",
          borderRadius: 8,
          cursor: "pointer",
          fontWeight: 700,
          userSelect: "none",
        }}
        onClick={onAddClick}
      >
        + Add Medication
      </button>

      {medications.length === 0 ? (
        <div
          style={{
            backgroundColor: "#F9FAFB",
            borderRadius: 18,
            padding: 48,
            textAlign: "center",
            color: "#6B7280",
            userSelect: "none",
          }}
        >
          <p style={{ fontSize: 24, fontWeight: 700, marginBottom: 12 }}>
            No Medications Added
          </p>
          <p style={{ fontSize: 16 }}>
            Start by adding your first medication to track your pill schedule and adherence
          </p>
        </div>
      ) : (
        <ul>
          {/* Medication items go here */}
        </ul>
      )}
    </>
  );
}

function AddMedicationModal({ onClose }: { onClose: () => void }) {
  const [name, setName] = React.useState("");
  const [dosage, setDosage] = React.useState("");
  const [stockCount, setStockCount] = React.useState(0);
  const [reminderTimes, setReminderTimes] = React.useState("");
  const [notes, setNotes] = React.useState("");
  const [notifyCaregiver, setNotifyCaregiver] = React.useState(false);

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    alert(`Added medication: ${name}`);
    onClose();
  }

  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(0,0,0,0.35)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1400,
      }}
    >
      <form
        onClick={(e) => e.stopPropagation()}
        onSubmit={handleSubmit}
        style={{
          backgroundColor: "white",
          borderRadius: 20,
          padding: 24,
          width: 400,
          fontFamily: "'Inter', sans-serif",
        }}
      >
        <h2 style={{ fontWeight: 700, fontSize: 24, marginBottom: 12 }}>Add New Medication</h2>
        <p style={{ fontSize: 14, marginBottom: 24 }}>
          Enter your medication details and reminder schedule
        </p>

        <label style={{ fontWeight: 600 }}>
          Medication Name *
          <input
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            type="text"
            placeholder="e.g., Metformin"
            style={{ width: "100%", padding: 8, marginTop: 4, marginBottom: 16, borderRadius: 6, border: "1px solid #D1D5DB" }}
          />
        </label>

        <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
          <label style={{ flex: 1, fontWeight: 600 }}>
            Dosage *
            <input
              required
              value={dosage}
              onChange={(e) => setDosage(e.target.value)}
              type="text"
              placeholder="e.g., 500mg"
              style={{ width: "100%", padding: 8, marginTop: 4, borderRadius: 6, border: "1px solid #D1D5DB" }}
            />
          </label>
          <label style={{ flex: 1, fontWeight: 600 }}>
            Stock Count *
            <input
              required
              value={stockCount}
              onChange={(e) => setStockCount(Number(e.target.value))}
              type="number"
              min={0}
              placeholder="30"
              style={{ width: "100%", padding: 8, marginTop: 4, borderRadius: 6, border: "1px solid #D1D5DB" }}
            />
          </label>
        </div>

        <label style={{ fontWeight: 600 }}>
          Frequency
          <input
            value={reminderTimes}
            onChange={(e) => setReminderTimes(e.target.value)}
            type="text"
            placeholder="Reminder Times, separated by commas"
            style={{ width: "100%", padding: 8, marginTop: 4, marginBottom: 16, borderRadius: 6, border: "1px solid #D1D5DB" }}
          />
        </label>

        <label style={{ fontWeight: 600 }}>
          Notes (Optional)
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="e.g., Take with food."
            style={{ width: "100%", padding: 8, borderRadius: 6, border: "1px solid #D1D5DB", marginBottom: 16 }}
          />
        </label>

        <label style={{ display: "flex", alignItems: "center", gap: 8, fontWeight: 600, marginBottom: 24 }}>
          <input
            type="checkbox"
            checked={notifyCaregiver}
            onChange={(e) => setNotifyCaregiver(e.target.checked)}
          />
          Notify caregiver
        </label>

        <div style={{ display: "flex", gap: 8 }}>
          <button
            type="submit"
            style={{
              flex: 1,
              backgroundColor: "#15803D",
              color: "white",
              borderRadius: 6,
              border: "none",
              padding: 12,
              fontWeight: 700,
              cursor: "pointer",
            }}
          >
            Add Medication
          </button>
          <button
            type="button"
            onClick={onClose}
            style={{
              flex: 1,
              backgroundColor: "#F3F4F6",
              borderRadius: 6,
              border: "1px solid #D1D5DB",
              padding: 12,
              cursor: "pointer",
              fontWeight: 600,
            }}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
