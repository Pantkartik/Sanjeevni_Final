import React, { useState } from "react";

const posts = [
  {
    id: 1,
    author: "Sarah M.",
    time: "2 hours ago",
    content: "Just completed my 30-day meditation challenge! The mental health benefits are incredible. My anxiety levels have decreased significantly, and I'm sleeping better.",
    tags: ["Mental Health", "meditation", "anxiety", "sleep"],
    likes: 24,
    comments: 8,
  },
  {
    id: 2,
    author: "Dr. Rajesh K.",
    time: "4 hours ago",
    content: "Quick tip for diabetes management: Pair carbs with protein or healthy fats. Helps prevent spikes. Combinations like apple with almond butter work great.",
    tags: ["Expert", "diabetes", "nutrition", "blood sugar"],
    likes: 45,
    comments: 12,
  },
];

const groups = [
  {
    id: 1,
    name: "Diabetes Support Circle",
    description: "Supportive community for diabetes management",
    tags: ["Chronic Conditions"],
    members: 1247,
    lastActive: "2 minutes ago",
    joined: true,
  },
  {
    id: 2,
    name: "Mental Health Warriors",
    description: "Support and share wins in mental health journeys",
    tags: ["Mental Health"],
    members: 892,
    lastActive: "15 minutes ago",
    joined: false,
  },
  {
    id: 3,
    name: "Heart Health Heroes",
    description: "Tips and encouragement for cardiovascular health",
    tags: ["Heart Health"],
    members: 634,
    lastActive: "1 hour ago",
    joined: true,
  },
  {
    id: 4,
    name: "New Parent Support",
    description: "Navigate parenthood with health & wellness focus",
    tags: ["Family Health"],
    members: 456,
    lastActive: "3 hours ago",
    joined: false,
  },
];

export default function Community() {
  const [activeTab, setActiveTab] = useState("Feed");
  const [newPost, setNewPost] = useState("");
  const [showPostModal, setShowPostModal] = useState(false);

  function handlePostSubmit() {
    alert("Post shared to community!");
    setShowPostModal(false);
    setNewPost("");
  }

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Sidebar (can reuse Sidebar component) */}
      {/* Main Content */}
      <main style={{ flex: 1, padding: 32, fontFamily: "'Inter', sans-serif" }}>
        <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
          <h1>Community</h1>
          <button
            style={{
              backgroundColor: "#15803D",
              color: "white",
              borderRadius: 12,
              padding: "8px 16px",
              fontWeight: 600,
              cursor: "pointer",
            }}
            onClick={() => setShowPostModal(true)}
          >
            New Post
          </button>
        </header>

        {/* Tabs */}
        <nav style={{ borderBottom: "1px solid #D1D5DB", marginBottom: 24, display: "flex", gap: 16 }}>
          {["Feed", "Support Groups", "Challenges", "Live Chat"].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                padding: "8px 24px",
                borderRadius: 12,
                border: "none",
                backgroundColor: activeTab === tab ? "#F3F4F6" : "transparent",
                fontWeight: activeTab === tab ? 700 : 500,
                cursor: "pointer",
              }}
            >
              {tab}
            </button>
          ))}
        </nav>

        {activeTab === "Feed" && (
          <section>
            {posts.map((post) => (
              <Post key={post.id} post={post} />
            ))}
          </section>
        )}

        {activeTab === "Support Groups" && (
          <section style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 20 }}>
            {groups.map((group) => (
              <GroupCard key={group.id} group={group} />
            ))}
          </section>
        )}

        {/* similarly implement Challenges and Live Chat tabs if needed */}

        {showPostModal && (
          <Modal onClose={() => setShowPostModal(false)}>
            <PostForm newPost={newPost} setNewPost={setNewPost} onSubmit={handlePostSubmit} onCancel={() => setShowPostModal(false)} />
          </Modal>
        )}
      </main>
    </div>
  );
}

function Post({ post }: { post: any }) {
  return (
    <article style={{ backgroundColor: "white", borderRadius: 16, padding: 24, marginBottom: 16, boxShadow: "0 5px 18px rgba(0,0,0,0.06)" }}>
      <header style={{ marginBottom: 12 }}>
        <strong>{post.author}</strong>
        {post.author.includes("Dr.") && <span style={{ marginLeft: 8, backgroundColor: "#065f46", color: "white", borderRadius: 4, padding: "2px 6px", fontSize: 12 }}>Expert</span>}
        <span style={{ marginLeft: 8, color: "#6b7280" }}>{post.time}</span>
      </header>
      <p style={{ marginBottom: 12 }}>{post.content}</p>
      {post.image && <img src={post.image} alt="" style={{ width: "100%", borderRadius: 12, marginBottom: 12 }} />}
      <footer style={{ color: "#6b7280", display: "flex", gap: 24 }}>
        <span>❤️ {post.likes}</span>
        <span>💬 {post.comments}</span>
        <span>🔗 Share</span>
      </footer>
    </article>
  );
}

function GroupCard({ group }: { group: any }) {
  return (
    <article style={{ backgroundColor: "white", borderRadius: 16, padding: 24, boxShadow: "0 5px 18px rgba(0,0,0,0.06)" }}>
      <header style={{ marginBottom: 8, display: "flex", justifyContent: "space-between" }}>
        <h3>{group.name}</h3>
        <span style={{ backgroundColor: "#d1fae5", color: "#065f46", borderRadius: 12, padding: "4px 8px", fontSize: 12 }}>
          {group.tags.join(", ")}
        </span>
      </header>
      <p style={{ color: "#6b7280", fontSize: 14, marginBottom: 12 }}>{group.description}</p>
      <div style={{ color: "#374151" }}>{group.members.toLocaleString()} members</div>
      <div style={{ color: "#6b7280", fontSize: 12, marginBottom: 16 }}>{group.lastActive}</div>
      <button
        style={{
          backgroundColor: group.joined ? "#465e43" : "#15803D",
          color: "white",
          borderRadius: 6,
          padding: "8px 16px",
          fontWeight: 600,
          cursor: "pointer",
          width: "100%",
          border: "none",
          marginBottom: 8,
        }}
      >
        {group.joined ? "Joined" : "Join Group"}
      </button>
    </article>
  );
}

function Modal({ children, onClose }: { children: React.ReactNode; onClose: () => void }) {
  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(0,0,0,0.4)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1500,
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          backgroundColor: "white",
          borderRadius: 20,
          padding: 24,
          width: 400,
          maxWidth: "95vw",
        }}
      >
        {children}
      </div>
    </div>
  );
}

function PostForm({
  newPost,
  setNewPost,
  onSubmit,
  onCancel,
}: {
  newPost: string;
  setNewPost: (value: string) => void;
  onSubmit: () => void;
  onCancel: () => void;
}) {
  return (
    <>
      <h2 style={{ fontSize: 23, marginBottom: 24 }}>Share with Community</h2>
      <textarea
        rows={4}
        value={newPost}
        onChange={(e) => setNewPost(e.target.value)}
        placeholder="Share your health journey, tips, or ask for support"
        style={{ width: "100%", borderRadius: 12, border: "1px solid #d1d5db", padding: 16, fontSize: 16, resize: "none" }}
      />
      <div style={{ marginTop: 16, display: "flex", justifyContent: "space-between" }}>
        <div>
          <button type="button" style={{ marginRight: 8 }}>
            📷 Add Photo
          </button>
          <button type="button">😊 Add Emoji</button>
        </div>
        <div>
          <button
            type="button"
            onClick={onSubmit}
            style={{
              backgroundColor: "#15803D",
              color: "white",
              fontWeight: 700,
              padding: "8px 24px",
              borderRadius: 12,
              cursor: "pointer",
            }}
          >
            Share Post
          </button>
        </div>
      </div>
      <button
        type="button"
        onClick={onCancel}
        style={{ marginTop: 16, background: "transparent", border: "none", color: "#374151", cursor: "pointer", fontWeight: 600 }}
      >
        Cancel
      </button>
    </>
  );
}
