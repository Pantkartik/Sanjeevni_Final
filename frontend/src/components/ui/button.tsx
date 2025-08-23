interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline";
  children: React.ReactNode;
  className?: string;
}

export function Button({ variant = "default", children, className, ...props }: ButtonProps) {
  const baseClass = "btn";
  const variantClass = variant === "default" ? "btn-success" : "btn-outline-secondary";
  return (
    <button className={`${baseClass} ${variantClass} ${className ?? ""}`} {...props}>
      {children}
    </button>
  );
}
