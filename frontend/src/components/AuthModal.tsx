import React, { useEffect, useRef } from "react";

interface AuthModalProps {
  open: boolean;
  mode: "signup" | "login";
  onClose: () => void;
  switchMode: (mode: "signup" | "login") => void;
  onLoginSuccess: () => void;
}

export default function AuthModal({ open, mode, onClose, switchMode, onLoginSuccess }: AuthModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    modalRef.current?.focus();
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      tabIndex={-1}
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(0,0,0,0.4)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1300,
      }}
      onClick={onClose}
      aria-modal="true"
      role="dialog"
    >
      <div
        ref={modalRef}
        tabIndex={0}
        onClick={(e) => e.stopPropagation()}
        style={{
          backgroundColor: "#fff",
          borderRadius: 20,
          padding: 30,
          width: 420,
          maxWidth: "95vw",
          boxShadow: "0 8px 32px rgba(0,0,0,0.2)",
          outline: "none",
          fontFamily: "'Inter', sans-serif",
        }}
      >
        <h2 style={{ textAlign: "center", fontWeight: 700, fontSize: 24, marginBottom: 8 }}>
          Join Sanjeevni Today
        </h2>
        <p style={{ textAlign: "center", color: "#4B5563", marginBottom: 24 }}>
          Start your journey to better health with AI-powered insights
        </p>

        <div
          style={{
            backgroundColor: "#FEF3C7",
            border: "1px solid #FCD34D",
            borderRadius: 12,
            padding: 12,
            color: "#92400E",
            display: "flex",
            alignItems: "center",
            gap: 8,
            marginBottom: 24,
            fontSize: 14,
          }}
        >
          <svg
            width={20}
            height={20}
            fill="none"
            stroke="#92400E"
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
            viewBox="0 0 24 24"
          >
            <path d="M10 2 L17 15 L10 10 L3 15 Z" />
          </svg>
          This is a prototype platform. Always consult healthcare professionals for medical advice.
        </div>

        {/* Sign Up & Login Tabs */}
        <div style={{ display: "flex", marginBottom: 24 }}>
          <button
            onClick={() => switchMode("signup")}
            style={{
              flex: 1,
              padding: 12,
              border: "1.8px solid #D1D5DB",
              backgroundColor: mode === "signup" ? "#fff" : "transparent",
              fontWeight: 600,
              borderTopLeftRadius: 12,
              borderBottomLeftRadius: 12,
              borderRight: "none",
              cursor: "pointer",
              color: mode === "signup" ? "#111827" : "#4B5563",
            }}
          >
            Sign Up
          </button>
          <button
            onClick={() => switchMode("login")}
            style={{
              flex: 1,
              padding: 12,
              border: "1.8px solid #D1D5DB",
              backgroundColor: mode === "login" ? "#fff" : "transparent",
              fontWeight: 600,
              borderTopRightRadius: 12,
              borderBottomRightRadius: 12,
              cursor: "pointer",
              color: mode === "login" ? "#111827" : "#4B5563",
            }}
          >
            Login
          </button>
        </div>

        {mode === "signup" ? <SignUpForm onCancel={onClose} /> : <LoginForm onLoginSuccess={onLoginSuccess} onCancel={onClose} />}
      </div>
    </div>
  );
}

function UploadIcon() {
  return (
    <svg width={40} height={40} fill="none" viewBox="0 0 24 24">
      <rect x={4} y={16} width={16} height={4} rx={2} fill="#DCFCE7" stroke="#22C55E" strokeWidth={1} />
      <path
        stroke="#22C55E"
        strokeWidth={2}
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12 4v10m-4-4 4-4 4 4"
      />
    </svg>
  );
}

function SignUpForm({ onCancel }: { onCancel: () => void }) {
  const [fullName, setFullName] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    alert(`Signed Up: ${fullName}, ${email}`);
  }

  return (
    <form onSubmit={handleSubmit}>
      <div style={{ color: "#374151", marginBottom: 16, fontWeight: 600 }}>
        Profile Photo (Optional)
      </div>
      <div style={{ display: "flex", justifyContent: "center", marginBottom: 24 }}>
        <UploadIcon />
      </div>
      <div style={{ display: "flex", justifyContent: "center", marginBottom: 24 }}>
        <button
          type="button"
          style={{
            padding: "10px 20px",
            borderRadius: 8,
            border: "1.8px solid #D1D5DB",
            backgroundColor: "#fff",
            color: "#374151",
            fontWeight: 600,
            cursor: "pointer",
          }}
        >
          Upload Photo
        </button>
      </div>

      <label style={{ fontWeight: 600, marginBottom: 4 }}>Full Name</label>
      <input
        type="text"
        placeholder="Enter full name"
        required
        value={fullName}
        onChange={(e) => setFullName(e.target.value)}
        style={{
          width: "100%",
          padding: 8,
          fontSize: 16,
          borderRadius: 8,
          border: "1.8px solid #D1D5DB",
          marginBottom: 16,
        }}
      />

      <label style={{ fontWeight: 600, marginBottom: 4 }}>Email</label>
      <input
        type="email"
        placeholder="Enter email"
        required
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={{
          width: "100%",
          padding: 8,
          fontSize: 16,
          borderRadius: 8,
          border: "1.8px solid #D1D5DB",
          marginBottom: 16,
        }}
      />

      <label style={{ fontWeight: 600, marginBottom: 4 }}>Password</label>
      <input
        type="password"
        placeholder="Create password"
        required
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{
          width: "100%",
          padding: 8,
          fontSize: 16,
          borderRadius: 8,
          border: "1.8px solid #D1D5DB",
          marginBottom: 24,
        }}
      />

      <button
        type="submit"
        style={{
          width: "100%",
          backgroundColor: "#15803D",
          color: "#fff",
          padding: 12,
          borderRadius: 8,
          fontWeight: 700,
          fontSize: "1.125rem",
          cursor: "pointer",
          boxShadow: "0 8px 24px rgba(22, 163, 74, 0.48)",
          userSelect: "none",
        }}
      >
        Create Account
      </button>

      <p style={{ fontSize: 12, color: "#6B7280", marginTop: 8, userSelect: "none" }}>
        By signing up, you agree to our Terms of Service and Privacy Policy.
      </p>

      <div
        onClick={onCancel}
        style={{
          marginTop: 16,
          color: "#374151",
          fontWeight: 600,
          textAlign: "center",
          cursor: "pointer",
          userSelect: "none",
        }}
      >
        Cancel
      </div>
    </form>
  );
}

function LoginForm({ onLoginSuccess, onCancel }: { onLoginSuccess: () => void; onCancel: () => void }) {
  const [userEmail, setUserEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [loading, setLoading] = React.useState(false);

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setLoading(true);

    // Simulate async login
    setTimeout(() => {
      setLoading(false);
      alert(`Logged in as ${userEmail}`);
      onLoginSuccess();
    }, 1500);
  }

  return (
    <form onSubmit={handleSubmit}>
      <div style={{ color: "#374151", marginBottom: 16, fontWeight: 600 }}>
        Profile Photo (Optional)
      </div>
      <div style={{ display: "flex", justifyContent: "center", marginBottom: 24 }}>
        <UploadIcon />
      </div>
      <div style={{ display: "flex", justifyContent: "center", marginBottom: 24 }}>
        <button
          type="button"
          style={{
            padding: "10px 20px",
            borderRadius: 8,
            border: "1.8px solid #D1D5DB",
            backgroundColor: "#fff",
            color: "#374151",
            fontWeight: 600,
            cursor: "pointer",
          }}
        >
          Upload Photo
        </button>
      </div>

      <label style={{ fontWeight: 600, marginBottom: 4 }}>Username or Email</label>
      <input
        type="text"
        placeholder="Enter username or email"
        required
        value={userEmail}
        onChange={(e) => setUserEmail(e.target.value)}
        style={{
          width: "100%",
          padding: 8,
          fontSize: 16,
          borderRadius: 8,
          border: "1.8px solid #D1D5DB",
          marginBottom: 16,
        }}
      />

      <label style={{ fontWeight: 600, marginBottom: 4 }}>Password</label>
      <input
        type="password"
        placeholder="Enter password"
        required
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{
          width: "100%",
          padding: 8,
          fontSize: 16,
          borderRadius: 8,
          border: "1.8px solid #D1D5DB",
          marginBottom: 24,
        }}
      />

      <button
        type="submit"
        disabled={loading}
        style={{
          width: "100%",
          backgroundColor: "#15803D",
          color: "#fff",
          padding: 12,
          borderRadius: 8,
          fontWeight: 700,
          fontSize: "1.125rem",
          cursor: loading ? "not-allowed" : "pointer",
          boxShadow: "0 8px 24px rgba(22, 163, 74, 0.48)",
          userSelect: "none",
        }}
      >
        {loading ? "Logging in..." : "Sign In"}
      </button>

      <p
        onClick={() => alert("Password reset flow")}
        style={{
          fontSize: 14,
          color: "#15803D",
          textAlign: "center",
          marginTop: 12,
          cursor: "pointer",
          userSelect: "none",
        }}
      >
        Forgot password?
      </p>

      <div
        onClick={onCancel}
        style={{
          marginTop: 16,
          color: "#374151",
          fontWeight: 600,
          textAlign: "center",
          cursor: "pointer",
          userSelect: "none",
        }}
      >
        Cancel
      </div>
    </form>
  );
}
