export default function HeroSection() {
  return (
    <div className="container py-5 text-center fade-in">
      <span className="badge bg-success mb-3 fs-6">AI-Powered Healthcare Platform</span>
      <h1 className="display-4 fw-bold mb-4">Your Complete Health Companion</h1>
      <p className="lead text-muted mb-5">
        Sanjeevni combines AI-powered health predictions, smart pill reminders, mental health tracking, and teleconsultation in one comprehensive platform designed for the Indian healthcare ecosystem.
      </p>
      <div className="hero-buttons">
        <button className="btn btn-success btn-lg btn-scale">Get Started Free</button>
        <button className="btn btn-outline-secondary btn-lg btn-scale">
          <svg width="18" height="18" fill="none" viewBox="0 0 20 20" className="me-2">
            <polygon points="7,5 15,10 7,15" fill="#198754" />
          </svg>
          Watch Demo
        </button>
      </div>
    </div>
  );
}
