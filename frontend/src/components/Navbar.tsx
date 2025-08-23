import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-white border-bottom fixed-top" style={{ marginTop: "30px", zIndex: 100 }}>
      <div className="container">
        <Link to="/" className="navbar-brand d-flex align-items-center gap-2 fw-semibold">
          <div className="bg-success rounded p-1 d-flex align-items-center justify-content-center" style={{width: "28px", height: "28px"}}>
            <svg width="18" height="18" fill="white" viewBox="0 0 20 20">
              <path d="M10 17s6.875-4.625 7.875-8C18.875 5.625 15.375 3 10 8.125C4.625 3 1.125 5.625 2.125 9C3.125 12.375 10 17 10 17z"/>
            </svg>
          </div>
          Sanjeevni
        </Link>

        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu" aria-controls="navMenu" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse justify-content-center" id="navMenu">
          <ul className="navbar-nav text-muted fw-semibold">
            <li className="nav-item"><Link className="nav-link" to="/features">Features</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/testimonials">Testimonials</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/about">About</Link></li>
          </ul>
        </div>

        <div className="d-flex gap-2">
          <Link to="/login" className="btn btn-link text-dark fw-semibold">Login</Link>
          <Link to="/signup" className="btn btn-success fw-semibold">Sign Up</Link>
        </div>
      </div>
    </nav>
  );
}
