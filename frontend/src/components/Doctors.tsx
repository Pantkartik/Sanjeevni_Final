// import React, { useState } from "react";

// const doctorProfiles = [
//   {
//     id: 1,
//     code: "DSP",
//     name: "Dr. Sarah Patel",
//     specialization: "Cardiologist",
//     rating: 4.8,
//     reviews: 124,
//     experience: 15,
//     hospital: "Apollo Hospital",
//     location: "Mumbai, Maharashtra",
//     nextAvailable: "Today 3:00 PM",
//     languages: ["English", "Hindi"],
//     fee: 800,
//     confirmed: true,
//   },
//   {
//     id: 2,
//     code: "DRK",
//     name: "Dr. Rajesh Kumar",
//     specialization: "Endocrinologist",
//     rating: 4.7,
//     reviews: 89,
//     experience: 12,
//     hospital: "Fortis Healthcare",
//     location: "Delhi, NCR",
//     nextAvailable: "Tomorrow 10:00 AM",
//     languages: ["English", "Hindi"],
//     fee: 1200,
//     completed: true,
//   },
// ];

// export default function Doctors() {
//   const [search, setSearch] = useState("");
//   const [specialty, setSpecialty] = useState("All specialties");
//   const [location, setLocation] = useState("All locations");

//   // Filtered doctors mock logic
//   const filteredDoctors = doctorProfiles.filter((doc) => {
//     const inSearch = doc.name.toLowerCase().includes(search.toLowerCase()) || doc.specialization.toLowerCase().includes(search.toLowerCase());
//     const inSpecialty = specialty === "All specialties" || doc.specialization === specialty;
//     const inLocation = location === "All locations" || doc.location === location;
//     return inSearch && inSpecialty && inLocation;
//   });

//   return (
//     <div style={{ marginLeft: 240, padding: 32, fontFamily: "'Inter', sans-serif", maxWidth: 1200 }}>
//       <h1 style={{ fontWeight: 700, fontSize: 28, marginBottom: 20 }}>Find Doctors</h1>
//       <section style={{ marginBottom: 24 }}>
//         <div style={{ display: "flex", gap: 16 }}>
//           <input
//             type="search"
//             placeholder="Doctor name or specialty"
//             value={search}
//             onChange={(e) => setSearch(e.target.value)}
//             style={{
//               flexGrow: 1,
//               padding: 12,
//               borderRadius: 8,
//               border: "1.5px solid #D1D5DB",
//               fontSize: 16,
//               outline: "none",
//             }}
//           />
//           <select value={specialty} onChange={(e) => setSpecialty(e.target.value)} style={{ padding: 12, borderRadius: 8, border: "1.5px solid #D1D5DB", fontSize: 16 }}>
//             <option>All specialties</option>
//             <option>Cardiologist</option>
//             <option>Endocrinologist</option>
//             <option>Dermatologist</option>
//             {/* add as per your data */}
//           </select>
//           <select value={location} onChange={(e) => setLocation(e.target.value)} style={{ padding: 12, borderRadius: 8, border: "1.5px solid #D1D5DB", fontSize: 16 }}>
//             <option>All locations</option>
//             <option>Mumbai, Maharashtra</option>
//             <option>Delhi, NCR</option>
//             <option>Bangalore, Karnataka</option>
//             {/* add as per your data */}
//           </select>
//           <button
//             type="button"
//             onClick={() => alert("Search triggered")}
//             style={{
//               backgroundColor: "#15803D",
//               color: "white",
//               padding: "12px 24px",
//               borderRadius: 8,
//               border: "none",
//               fontWeight: 700,
//               cursor: "pointer",
//             }}
//           >
//             Search
//           </button>
//         </div>
//       </section>
//       <nav style={{ marginBottom: 24, display: "flex", gap: 10 }}>
//         <button style={{ flexGrow: 1, padding: 12, borderRadius: 8, backgroundColor: "#F3F4F6", fontWeight: 600 }}>Find Doctors</button>
//         <button style={{ flexGrow: 1, padding: 12, borderRadius: 8, border: "1.5px solid #D1D5DB" }}>My Appointments</button>
//         <button style={{ flexGrow: 1, padding: 12, borderRadius: 8, border: "1.5px solid #D1D5DB" }}>Teleconsultation</button>
//       </nav>

//       {filteredDoctors.map((doc) => (
//         <div key={doc.id} style={{ backgroundColor: "#F9FBFC", borderRadius: 20, padding: 24, marginBottom: 24, boxShadow: "0 7px 24px rgba(12,41,29,0.05)" }}>
//           <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
//             <div>
//               <span style={{ fontWeight: 700, fontSize: 16 }}>{doc.code}</span> - <span style={{ fontWeight: 600, fontSize: 24 }}>{doc.name}</span>
//             </div>
//             <div>
//               <span style={{ fontWeight: 600, fontSize: 18, color: "#15803D" }}>{`₹${doc.fee}`}</span> <br />
//               <small>Consultation fee</small>
//             </div>
//           </div>
//           <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
//             <div>Specialty: {doc.specialization}</div>
//             <div>Rating: ⭐ {doc.rating} ({doc.reviews} reviews)</div>
//             <div>Experience: {doc.experience} years</div>
//             <div>Hospital: {doc.hospital}</div>
//             <div>Location: {doc.location}</div>
//             <div>Next Available: {doc.nextAvailable}</div>
//             <div>Languages: {doc.languages.join(", ")}</div>
//           </div>
//           <div style={{ marginTop: 12, display: "flex", gap: 12 }}>
//             <button
//               type="button"
//               style={{
//                 backgroundColor: "#15803D",
//                 color: "white",
//                 padding: "10px 24px",
//                 borderRadius: 8,
//                 border: "none",
//                 fontWeight: 600,
//                 cursor: "pointer",
//               }}
//               onClick={() => alert(`Joining video call with ${doc.name}`)}
//             >
//               Join Video Call
//             </button>
//             <button
//               type="button"
//               style={{
//                 padding: "10px 24px",
//                 borderRadius: 8,
//                 border: "1.5px solid #D1D5DB",
//                 fontWeight: 600,
//                 cursor: "pointer",
//                 backgroundColor: "white",
//               }}
//               onClick={() => alert(`Messaging ${doc.name}`)}
//             >
//               Message Doctor
//             </button>
//             <button
//               type="button"
//               style={{
//                 padding: "10px 24px",
//                 borderRadius: 8,
//                 border: "1.5px solid #D1D5DB",
//                 fontWeight: 600,
//                 cursor: "pointer",
//                 backgroundColor: "white",
//               }}
//               onClick={() => alert(`Rescheduling appointment with ${doc.name}`)}
//             >
//               Reschedule
//             </button>
//           </div>
//         </div>
//       ))}
//     </div>
//   );
// }




// Doctors.tsx (your full doctor search/list component as provided)
import React, { useState } from "react";

export default function Doctors() {
  // Your full Doctors component as provided
}
