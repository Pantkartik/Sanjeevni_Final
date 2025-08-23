// import React from "react";

// export default function Dashboard() {
//   return (
//     <div
//       style={{
//         marginLeft: 240,
//         padding: "28px 32px 30px 32px",
//         maxWidth: 1200,
//         fontFamily: "'Inter', sans-serif",
//       }}
//     >
//       <h1 style={{ fontWeight: 700, fontSize: 28, marginBottom: 12 }}>
//         Welcome back, kartikpant.kp69@gmail.com!
//       </h1>
//       <p style={{ color: "#4B5563", fontSize: 16, marginBottom: 28 }}>
//         Here’s your health overview for today
//       </p>

//       {/* Overview cards */}
//       <section
//         style={{
//           display: "flex",
//           gap: 16,
//           marginBottom: 28,
//           flexWrap: "wrap",
//           userSelect: "none",
//         }}
//       >
//         {[
//           {
//             title: "Pill Adherence",
//             value: "94%",
//             sub: "+2% from last week",
//             icon: "💊",
//             progress: 94,
//           },
//           {
//             title: "Health Score",
//             value: "8.2",
//             sub: "Excellent condition",
//             icon: "💓",
//             progress: 82,
//           },
//           {
//             title: "Mental Wellness",
//             value: "Good",
//             sub: "Stable mood trend",
//             icon: "🧠",
//             progress: 75,
//           },
//           {
//             title: "Next Appointment",
//             value: "2",
//             sub: "days remaining",
//             icon: "📅",
//             badge: "Dr. Sharma",
//           },
//         ].map(({ title, value, sub, icon, progress, badge }) => (
//           <div
//             key={title}
//             style={{
//               flex: "1 1 200px",
//               backgroundColor: "#F9FAFB",
//               borderRadius: 18,
//               boxShadow: "0 10px 24px rgba(0,0,0,0.07)",
//               padding: 24,
//               minWidth: 220,
//             }}
//           >
//             <div style={{ fontSize: 26, marginBottom: 16 }}>{icon}</div>
//             <h3
//               style={{
//                 fontWeight: 700,
//                 fontSize: 24,
//                 margin: 0,
//                 marginBottom: 6,
//                 color: "#111827",
//               }}
//             >
//               {title}
//             </h3>
//             <div style={{ fontWeight: 700, fontSize: 28, marginBottom: 6 }}>
//               {value}
//             </div>
//             <div style={{ color: "#4B5563", fontSize: 14, marginBottom: 6 }}>
//               {sub}
//             </div>
//             {badge && (
//               <div
//                 style={{
//                   display: "inline-block",
//                   backgroundColor: "#15803d",
//                   color: "#fff",
//                   padding: "2px 8px",
//                   borderRadius: 8,
//                   fontSize: 13,
//                   fontWeight: 600,
//                   userSelect: "none",
//                 }}
//               >
//                 {badge}
//               </div>
//             )}

//             <div
//               style={{
//                 backgroundColor: "#D1FAE5",
//                 height: 8,
//                 borderRadius: 6,
//                 width: "100%",
//                 marginTop: 8,
//                 overflow: "hidden",
//               }}
//             >
//               <div
//                 style={{
//                   width: `${progress}%`,
//                   height: 8,
//                   backgroundColor: "#15803d",
//                   borderRadius: 6,
//                   transition: "width 0.4s ease",
//                 }}
//               />
//             </div>
//           </div>
//         ))}
//       </section>

//       {/* Quick actions and recent alerts */}
//       <section style={{ display: "flex", gap: 24, marginBottom: 28 }}>
//         <div
//           style={{
//             flex: 2,
//             backgroundColor: "#F9FAFB",
//             borderRadius: 18,
//             padding: 24,
//             boxShadow: "0 10px 24px rgba(0,0,0,0.07)",
//             userSelect: "none",
//           }}
//         >
//           <h4 style={{ fontWeight: 600, fontSize: 20, marginBottom: 12 }}>
//             Today's Schedule
//           </h4>
//           <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
//             {[
//               {
//                 title: "Metformin 500mg",
//                 desc: "Take with breakfast",
//                 badge: "8:00 AM",
//                 Icon: "💊",
//                 status: "done",
//               },
//               {
//                 title: "Lisinopril 10mg",
//                 desc: "Blood pressure medication",
//                 badge: "2:00 PM",
//                 Icon: "💊",
//                 status: "pending",
//               },
//               {
//                 title: "Teleconsultation",
//                 desc: "Follow-up with Dr. Patel",
//                 badge: "4:30 PM",
//                 Icon: "📞",
//                 status: "pending",
//               },
//             ].map(({ title, desc, badge, Icon, status }) => (
//               <li
//                 key={title}
//                 style={{
//                   display: "flex",
//                   justifyContent: "space-between",
//                   padding: "14px 0",
//                   borderBottom: "1px solid #E5E7EB",
//                   alignItems: "center",
//                 }}
//               >
//                 <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
//                   <span style={{ fontSize: 22 }}>{Icon}</span>
//                   <div>
//                     <div style={{ fontWeight: 600 }}>{title}</div>
//                     <div style={{ fontSize: 14, color: "#4B5563" }}>{desc}</div>
//                   </div>
//                 </div>
//                 <div
//                   style={{
//                     color: status === "done" ? "#15803d" : "#6B7280",
//                     fontWeight: 600,
//                     fontSize: 14,
//                   }}
//                 >
//                   {badge}{" "}
//                   {status === "done" ? (
//                     <span style={{ marginLeft: 8, color: "#15803d" }}>✓</span>
//                   ) : (
//                     <span style={{ marginLeft: 8 }}>⏰</span>
//                   )}
//                 </div>
//               </li>
//             ))}
//           </ul>
//         </div>
//         <div
//           style={{
//             flex: 1,
//             backgroundColor: "#F9FAFB",
//             borderRadius: 18,
//             padding: 24,
//             boxShadow: "0 10px 24px rgba(0,0,0,0.07)",
//             userSelect: "none",
//           }}
//         >
//           <h4 style={{ fontWeight: 600, fontSize: 20, marginBottom: 12 }}>
//             Quick Actions
//           </h4>
//           <ul
//             style={{
//               listStyle: "none",
//               paddingLeft: 0,
//               margin: 0,
//               display: "flex",
//               flexDirection: "column",
//               gap: 10,
//             }}
//           >
//             {[
//               "AI Health Scan",
//               "Mood Check-in",
//               "Book Consultation",
//               "Community Chat",
//             ].map((action) => (
//               <li
//                 key={action}
//                 style={{
//                   backgroundColor: "#fff",
//                   borderRadius: 12,
//                   padding: "12px 16px",
//                   border: "1.5px solid #D1D5DB",
//                   cursor: "pointer",
//                   fontWeight: 600,
//                   color: "#374151",
//                   textAlign: "center",
//                   userSelect: "none",
//                 }}
//               >
//                 {action}
//               </li>
//             ))}
//           </ul>
//           <h4 style={{ fontWeight: 600, fontSize: 20, marginTop: 24, marginBottom: 12 }}>
//             Recent Alerts
//           </h4>
//           <ul style={{ listStyle: "none", paddingLeft: 0, margin: 0 }}>
//             {[
//               {
//                 title: "Medication Taken",
//                 description: "Metformin taken on time",
//                 icon: "✔️",
//                 bg: "#DCFCE7",
//               },
//               {
//                 title: "Health Improvement",
//                 description: "Blood pressure trending down",
//                 icon: "↗️",
//                 bg: "#DCFCE7",
//               },
//               {
//                 title: "Appointment Reminder",
//                 description: "Dr. Sharma in 2 days",
//                 icon: "⚠️",
//                 bg: "#FCDDDE",
//               },
//             ].map(({ title, description, icon, bg }) => (
//               <li
//                 key={title}
//                 style={{
//                   backgroundColor: bg,
//                   borderRadius: 12,
//                   padding: 16,
//                   marginBottom: 8,
//                   userSelect: "none",
//                 }}
//               >
//                 <div style={{ fontWeight: 600, marginBottom: 4 }}>{title}</div>
//                 <div style={{ color: "#4B5563", fontSize: 14 }}>
//                   {icon} {description}
//                 </div>
//               </li>
//             ))}
//           </ul>
//         </div>
//       </section>

//       {/* Health Trends Chart placeholder */}
//       <section
//         style={{
//           marginTop: 12,
//           marginBottom: 36,
//           backgroundColor: "#F9FAFB",
//           borderRadius: 18,
//           padding: 24,
//           boxShadow: "0 10px 24px rgba(0,0,0,0.07)",
//           userSelect: "none",
//         }}
//       >
//         <h3 style={{ fontWeight: 700, fontSize: 24, marginBottom: 12 }}>
//           Health Trends
//         </h3>
//         <p style={{ color: "#4B5563", bodyFontSize: 16 }}>
//           Your health metrics over time
//         </p>
//         <div
//           style={{
//             marginTop: 24,
//             display: "flex",
//             justifyContent: "space-between",
//             gap: 20,
//             flexWrap: "wrap",
//           }}
//         >
//           {[
//             {
//               label: "Blood Pressure",
//               value: "120/80 mmHg",
//               percent: 70,
//               color: "#15803D",
//               icon: "📟",
//             },
//             {
//               label: "Blood Sugar",
//               value: "95 mg/dL",
//               percent: 85,
//               color: "#15803D",
//               icon: "🩸",
//             },
//             {
//               label: "Weight",
//               value: "72 kg",
//               percent: 70,
//               color: "#15803D",
//               icon: "⚖️",
//             },
//           ].map(({ label, value, percent, color, icon }) => (
//             <div
//               key={label}
//               style={{
//                 minWidth: 180,
//                 flex: "1 1 180px",
//                 backgroundColor: "#fff",
//                 borderRadius: 12,
//                 boxShadow: "0 6px 15px rgba(0,0,0,0.06)",
//                 padding: 18,
//               }}
//             >
//               <div
//                 style={{
//                   display: "flex",
//                   alignItems: "center",
//                   marginBottom: 12,
//                   fontWeight: 700,
//                   fontSize: 16,
//                   gap: 8,
//                   color: "#15803D",
//                 }}
//               >
//                 <span style={{ fontSize: 20 }}>{icon}</span> {label}
//               </div>
//               <div style={{ fontWeight: 600, fontSize: 20, marginBottom:8 }}>
//                 {value}
//               </div>
//               <div
//                 style={{
//                   backgroundColor: "#D1FAE5",
//                   height: 8,
//                   width: "100%",
//                   borderRadius: 6,
//                   overflow: "hidden",
//                 }}
//               >
//                 <div
//                   style={{
//                     height: 8,
//                     width: `${percent}%`,
//                     backgroundColor: color,
//                     borderRadius: 6,
//                     transition: "width 0.3s ease-in-out",
//                   }}
//                 ></div>
//               </div>
//             </div>
//           ))}
//         </div>
//       </section>
//     </div>
//   );
// }
// Dashboard.tsx (as provided)
import React from "react";

export default function Dashboard() {
  return (
    <div
      style={{
        marginLeft: 240,
        padding: "28px 32px 30px 32px",
        maxWidth: 1200,
        fontFamily: "'Inter', sans-serif",
      }}
    >
      <h1 style={{ fontWeight: 700, fontSize: 28, marginBottom: 12 }}>
        Welcome back, kartikpant.kp69@gmail.com!
      </h1>
      <p style={{ color: "#4B5563", fontSize: 16, marginBottom: 28 }}>
        Here’s your health overview for today
      </p>
      {/* Overview cards and other content as provided */}
      {/* ... */}
    </div>
  );
}
