import React, { useState, useEffect, useRef } from "react";

type Message = {
  id: number;
  userCode: string;
  userName: string;
  time: string;
  content: string;
};

export default function CommunityLiveChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      userCode: "DSP",
      userName: "Dr. Sarah P.",
      time: "10:30 AM",
      content: "Remember, consistency is key when managing blood pressure. Small daily actions make a big difference!",
    },
    {
      id: 2,
      userCode: "MR",
      userName: "Mike R.",
      time: "10:32 AM",
      content: "Thanks for the reminder! I've been tracking my BP daily & it's really helping me stay motivated.",
    },
    {
      id: 3,
      userCode: "LK",
      userName: "Lisa K.",
      time: "10:35 AM",
      content: "What’s everyone’s favorite healthy breakfast? Looking for new ideas to start my day right!",
    },
  ]);

  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom on new message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function sendMessage() {
    if (!input.trim()) return;
    const newMessage: Message = {
      id: messages.length + 1,
      userCode: "You",
      userName: "You",
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      content: input,
    };
    setMessages([...messages, newMessage]);
    setInput("");
  }

  return (
    <div
      style={{
        backgroundColor: "#F9FAFB",
        borderRadius: 18,
        boxShadow: "0 8px 32px rgba(0,0,0,0.05)",
        padding: 24,
        maxWidth: 800,
        margin: "auto",
        display: "flex",
        flexDirection: "column",
        height: 500,
      }}
    >
      <div style={{ flexGrow: 1, overflowY: "auto", marginBottom: 12 }}>
        {messages.map(({ id, userCode, userName, time, content }) => (
          <div key={id} style={{ marginBottom: 20 }}>
            <div style={{ fontWeight: "600", color: "#15803D" }}>{userCode} {userName} <span style={{ fontWeight: "normal", color: "#6B7280", marginLeft: 6 }}>{time}</span></div>
            <div style={{ color: "#374151", marginLeft: 20 }}>{content}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div style={{ display: "flex", gap: 10 }}>
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          style={{ flexGrow: 1, padding: 12, borderRadius: 10, border: "1.5px solid #D1D5DB", fontSize: 16 }}
        />
        <button
          onClick={() => sendMessage()}
          style={{
            backgroundColor: "#15803D",
            color: "white",
            borderRadius: 10,
            border: "none",
            padding: "12px 24px",
            fontWeight: 700,
            cursor: "pointer",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}
