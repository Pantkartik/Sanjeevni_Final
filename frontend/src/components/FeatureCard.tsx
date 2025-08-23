interface FeatureCardProps {
  icon: string;
  title: string;
  text: string;
}

export default function FeatureCard({ icon, title, text }: FeatureCardProps) {
  return (
    <div className="feature-card">
      <div className="feature-icon">{icon}</div>
      <h5 className="fw-semibold">{title}</h5>
      <p className="text-muted">{text}</p>
    </div>
  );
}
