import { Carousel } from "react-bootstrap";
import TestimonialCard from "./Testimonials";

const testimonials = [
  {
    stars: 5,
    text: "Sanjeevni’s pill reminders have been a game-changer for my elderly mother. The AI predictions caught a skin condition early that we might have missed.",
    name: "Priya Sharma",
    location: "Mumbai, Maharashtra",
    photo: "https://randomuser.me/api/portraits/women/65.jpg",
  },
  {
    stars: 5,
    text: "The mental health tracking feature helped me understand my stress patterns. The teleconsultation with doctors is seamless and convenient.",
    name: "Rajesh Kumar",
    location: "Bangalore, Karnataka",
    photo: "https://randomuser.me/api/portraits/men/43.jpg",
  },
  {
    stars: 5,
    text: "As a doctor, I appreciate how Sanjeevni helps my patients stay compliant with medications and provides valuable health insights between visits.",
    name: "Dr. Sneha Patel",
    location: "Delhi, NCR",
    photo: "https://randomuser.me/api/portraits/women/54.jpg",
  },
];

export default function TestimonialCards() {
  return (
    <section className="container py-5 fade-in delay-2">
      <h2 className="fw-bold text-center mb-4">Trusted by Thousands</h2>
      <p className="text-muted text-center mb-5">
        See how Sanjeevni is transforming healthcare experiences across India
      </p>
      <Carousel fade indicators={false} controls={false} interval={4000} pause={false}>
        {testimonials.map((t, idx) => (
          <Carousel.Item key={idx}>
            <TestimonialCard {...t} />
          </Carousel.Item>
        ))}
      </Carousel>
    </section>
  );
}
