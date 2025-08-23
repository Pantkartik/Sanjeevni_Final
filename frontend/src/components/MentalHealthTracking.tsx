// import React, { useState } from "react";

// export default function MentalHealthTracker() {
//   const [mood, setMood] = useState<number | null>(4);
//   const [stressLevel, setStressLevel] = useState(3);
//   const [anxietyLevel, setAnxietyLevel] = useState(2);

//   return (
//     <div
//       style={{
//         marginLeft: 240,
//         padding: "28px 32px",
//         maxWidth: 1200,
//         fontFamily: "'Inter', sans-serif",
//       }}
//     >
//       <h1 style={{ fontWeight: 700, fontSize: 28, marginBottom: 12 }}>
//         Mental Health Tracker
//       </h1>
//       <p style={{ color: "#4B5563", fontSize: 16, marginBottom: 24 }}>
//         Monitor your mental wellness and practice self-care
//       </p>

//       {/* Overview cards */}
//       <section style={{ display: "flex", gap: 16, flexWrap: "wrap", marginBottom: 24 }}>
//         <OverviewCard title="Current Mood" value="Good" icon="😊" description="Above average today" />
//         <OverviewCard title="Weekly Average" value="4.1" description="+0.3 from last week" icon="📈" />
//         <OverviewCard title="Exercises Completed" value="2/4" icon="🎯" description="Today's goal" />
//         <OverviewCard title="Streak" value="7" icon="🏅" description="Days tracking" />
//       </section>

//       {/* Tabs */}
//       <nav style={{ display: "flex", gap: 8, borderBottom: "1px solid #D1D5DB", marginBottom: 24 }} role="tablist" aria-orientation="horizontal">
//         {[          "Today",
//           "Exercises",
//           "Journal",
//           "Insights"
//         ].map((label, index) => (
//           <Tab
//             key={label}
//             label={label}
//             active={index === 0} // Default active on first tab, can be made dynamic
//             role="tab"
//             aria-selected={index === 0}
//             tabIndex={index === 0 ? 0 : -1}
//             id={`tab-${index}`}
//             aria-controls={`tabpanel-${index}`}
//             onClick={() => {
//               // implement tab switching logic here or lift state up as needed
//               console.log(`Switching to tab: ${label}`);
//             }}
//           />
//         ))}
//       </nav>

//       {/* Daily check-in form */}
//       <section style={{ display: "flex", gap: 24, flexWrap: "wrap", userSelect: "none" }}>
//         <div style={{ flex: 1, backgroundColor: "#F9FAFB", padding: 24, borderRadius: 18 }}>
//           <h3 style={{ fontWeight: 600, fontSize: 20, marginBottom: 12 }}>Daily Check-in</h3>

//           <div style={{ marginBottom: 12 }}>How are you feeling right now?</div>

//           {/* Mood selector */}
//           <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
//             {[1, 2, 3, 4, 5].map((val) => (
//               <button
//                 key={val}
//                 aria-label={`Mood ${val}`}
//                 onClick={() => setMood(val)}
//                 style={{
//                   width: 44,
//                   height: 44,
//                   borderRadius: 8,
//                   border: mood === val ? "2px solid #15803D" : "2px solid #E5E7EB",
//                   backgroundColor: mood === val ? "#D1FAE5" : "white",
//                   cursor: "pointer",
//                   fontSize: 24,
//                   userSelect: "none",
//                 }}
//               >
//                 {["😞", "☹️", "😐", "😊", "😀"][val - 1]}
//               </button>
//             ))}
//           </div>

//           {/* Stress & Anxiety sliders */}
//           <div style={{ marginBottom: 24 }}>
//             <label>
//               Stress Level
//               <input
//                 type="range"
//                 min={0}
//                 max={5}
//                 value={stressLevel}
//                 onChange={(e) => setStressLevel(parseInt(e.target.value))}
//                 style={{ width: "100%" }}
//               />
//             </label>
//             <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12 }}>
//               <span>Low</span>
//               <span>High</span>
//             </div>
//           </div>

//           <div style={{ marginBottom: 24 }}>
//             <label>
//               Anxiety Level
//               <input
//                 type="range"
//                 min={0}
//                 max={5}
//                 value={anxietyLevel}
//                 onChange={(e) => setAnxietyLevel(parseInt(e.target.value))}
//                 style={{ width: "100%" }}
//               />
//             </label>
//             <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12 }}>
//               <span>Low</span>
//               <span>High</span>
//             </div>
//           </div>

//           <button
//             type="button"
//             onClick={() => alert("Daily check-in saved!")}
//             style={{
//               backgroundColor: "#15803D",
//               color: "white",
//               fontSize: 18,
//               fontWeight: 700,
//               borderRadius: 8,
//               padding: "14px 0",
//               width: "100%",
//               cursor: "pointer",
//               userSelect: "none",
//             }}
//           >
//             Save Check-in
//           </button>
//         </div>

//         {/* Sidebar - relief and insights */}
//         <aside style={{ flexBasis: 300 }}>
//           <section
//             style={{
//               backgroundColor: "#F9FAFB",
//               padding: 24,
//               marginBottom: 24,
//               borderRadius: 18,
//               userSelect: "none",
//             }}
//           >
//             <h3 style={{ fontWeight: 600, fontSize: 20, marginBottom: 12 }}>Quick Relief</h3>
//             {[
//               "Breathing Exercise",
//               "Gratitude Practice",
//               "Mindfulness",
//               "Thought Record",
//             ].map((item) => (
//               <button
//                 key={item}
//                 type="button"
//                 style={{
//                   width: "100%",
//                   padding: 12,
//                   backgroundColor: "white",
//                   borderRadius: 8,
//                   marginBottom: 8,
//                   border: "1px solid #D1D5DB",
//                   textAlign: "left",
//                   fontWeight: 600,
//                   cursor: "pointer",
//                   userSelect: "none",
//                 }}
//               >
//                 {item}
//               </button>
//             ))}
//           </section>

//           <section
//             style={{
//               backgroundColor: "#FDE8E8",
//               padding: 24,
//               borderRadius: 18,
//               border: "1px solid #FCA5A5",
//               color: "#991B1B",
//               userSelect: "none",
//             }}
//           >
//             <h4 style={{ fontWeight: 700, marginBottom: 8 }}>Need Immediate Help?</h4>
//             <p style={{ marginBottom: 12 }}>Crisis support resources</p>
//             <button
//               type="button"
//               style={{
//                 backgroundColor: "#DC2626",
//                 color: "white",
//                 padding: 12,
//                 fontWeight: 700,
//                 borderRadius: 8,
//                 width: "100%",
//                 cursor: "pointer",
//                 userSelect: "none",
//               }}
//               onClick={() => alert("Calling crisis hotline")}
//             >
//               Crisis Hotline
//             </button>
//             {["Chat Support", "Ask Expert", "Health Tips"].map((help) => (
//               <button
//                 key={help}
//                 type="button"
//                 style={{
//                   width: "100%",
//                   padding: 12,
//                   backgroundColor: "white",
//                   borderRadius: 8,
//                   marginTop: 8,
//                   border: "1px solid #D1D5DB",
//                   textAlign: "left",
//                   fontWeight: 600,
//                   cursor: "pointer",
//                   userSelect: "none",
//                 }}
//                 onClick={() => alert(`Navigating to ${help}`)}
//               >
//                 {help}
//               </button>
//             ))}
//           </section>
//         </aside>
//       </section>
//     </div>
//   );
// }

// function OverviewCard({ title, value, icon, description }: { title: string; value: string | number; icon: string; description?: string; }) {
//   return (
//     <div
//       style={{
//         backgroundColor: "#F9FAFB",
//         borderRadius: 18,
//         padding: 24,
//         width: 200,
//         userSelect: "none",
//         boxShadow: "0 6px 15px rgba(0,0,0,0.06)",
//       }}
//     >
//       <div style={{ fontSize: 28, marginBottom: 12 }}>{icon}</div>
//       <div style={{ fontWeight: 600, fontSize: 14, color: "#6B7280", marginBottom: 4 }}>{title}</div>
//       <div style={{ fontSize: 20, fontWeight: 700, color: "#111827" }}>{value}</div>
//       {description && (
//         <div style={{ fontWeight: 400, fontSize: 14, marginTop: 6, color: "#6B7280" }}>
//           {description}
//         </div>
//       )}
//     </div>
//   );
// }




// MentalHealthTracking.tsx (your full component as provided)
import React, { useState } from "react";

export default function MentalHealthTracking() {
  // Your full MentalHealthTracker component code here unchanged
}
