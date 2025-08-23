// import React, { useState } from "react";

// type Appointment = {
//   id: number;
//   doctorName: string;
//   specialization: string;
//   type: "In-person" | "Teleconsultation";
//   fee: number;
//   date: string;
//   time: string;
//   status: "confirmed" | "pending" | "completed";
//   reason: string;
// };

// export default function AppointmentManagement() {
//   const [appointments, setAppointments] = useState<Appointment[]>([
//     {
//       id: 1,
//       doctorName: "Dr. Sarah Patel",
//       specialization: "Cardiologist",
//       type: "Teleconsultation",
//       fee: 800,
//       date: "2024-01-20",
//       time: "3:00 PM",
//       status: "confirmed",
//       reason: "Follow-up consultation",
//     },
//     {
//       id: 2,
//       doctorName: "Dr. Rajesh Kumar",
//       specialization: "Endocrinologist",
//       type: "In-person",
//       fee: 1200,
//       date: "2024-01-18",
//       time: "10:00 AM",
//       status: "completed",
//       reason: "Diabetes management",
//     },
//   ]);

//   return (
//     <div style={{ marginLeft: 240, padding: 32, maxWidth: 1200, fontFamily: "'Inter', sans-serif" }}>
//       <h1 style={{ fontWeight: 700, fontSize: 28, marginBottom: 24 }}>Appointments</h1>

//       <nav style={{ display: "flex", marginBottom: 24 }}>
//         <button style={tabButtonStyle(true)}>Upcoming</button>
//         <button style={tabButtonStyle(false)}>History</button>
//         <button style={tabButtonStyle(false)}>Teleconsultation</button>
//       </nav>

//       <div>
//         {appointments.map((appt) => (
//           <div
//             key={appt.id}
//             style={{
//               backgroundColor: "#F9FBFC",
//               borderRadius: 20,
//               padding: 24,
//               marginBottom: 24,
//               boxShadow: "0 7px 24px rgba(12,41,29,0.05)",
//               userSelect: "none",
//             }}
//           >
//             <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
//               <div>
//                 <span style={{ fontWeight: 700, fontSize: 20 }}>{appt.doctorName}</span>
//                 <div style={{ fontSize: 14, fontWeight: 600, color: "#374151" }}>{appt.specialization}</div>
//               </div>
//               <div style={{ fontWeight: 700, fontSize: 20 }}>₹{appt.fee}</div>
//             </div>

//             <div style={{ display: "flex", gap: 20, flexWrap: "wrap" }}>
//               <div>
//                 <strong>Date:</strong> {appt.date}
//               </div>
//               <div>
//                 <strong>Time:</strong> {appt.time}
//               </div>
//               <div>
//                 <strong>Type:</strong> {appt.type}
//               </div>
//               <div>
//                 <strong>Reason:</strong> {appt.reason}
//               </div>
//               <div style={{ flexGrow: 1 }}>
//                 <AppointmentStatusBadge status={appt.status} />
//               </div>
//             </div>

//             <div style={{ marginTop: 12, display: "flex", gap: 12 }}>
//               <button style={btnStyle("#15803D")} onClick={() => alert(`Joining video call with ${appt.doctorName}`)}>
//                 {appt.type === "Teleconsultation" ? "Join Video Call" : "View Details"}
//               </button>
//               <button style={btnOutlineStyle()} onClick={() => alert(`Messaging ${appt.doctorName}`)}>
//                 Message Doctor
//               </button>
//               <button style={btnOutlineStyle()} onClick={() => alert(`Rescheduling appointment with ${appt.doctorName}`)}>
//                 Reschedule
//               </button>
//             </div>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }

// function tabButtonStyle(active: boolean): React.CSSProperties {
//   return {
//     flex: 1,
//     padding: 12,
//     borderRadius: 12,
//     border: active ? "none" : "1.5px solid #D1D5DB",
//     backgroundColor: active ? "#F3F4F6" : "transparent",
//     fontWeight: active ? 700 : 500,
//     cursor: "pointer",
//   };
// }

// function btnStyle(color: string): React.CSSProperties {
//   return {
//     padding: "10px 24px",
//     borderRadius: 8,
//     backgroundColor: color,
//     color: "white",
//     fontWeight: 600,
//     border: "none",
//     cursor: "pointer",
//   };
// }

// function btnOutlineStyle(): React.CSSProperties {
//   return {
//     padding: "10px 24px",
//     borderRadius: 8,
//     backgroundColor: "white",
//     color: "#374151",
//     fontWeight: 600,
//     border: "1.5px solid #D1D5DB",
//     cursor: "pointer",
//   };
// }

// function AppointmentStatusBadge({ status }: { status: string }) {
//   const statusMap: Record<string, { text: string; color: string }> = {
//     confirmed: { text: "Confirmed", color: "#16A34A" },
//     pending: { text: "Pending", color: "#EAB308" },
//     completed: { text: "Completed", color: "#6B7280" },
//   };

//   const { text, color } = statusMap[status] || { text: status, color: "#374151" };

//   return (
//     <span
//       style={{
//         padding: "4px 10px",
//         borderRadius: 12,
//         backgroundColor: color,
//         color: "white",
//         fontWeight: 600,
//         fontSize: 14,
//         userSelect: "none",
//       }}
//     >
//       {text}
//     </span>
//   );
// }



// AppointmentManagement.tsx (your full component as provided)
import React, { useState } from "react";

export default function AppointmentManagement() {
  // Your full AppointmentManagement component as provided
}
