import React from "react";

export type ButtonVariant = "primary" | "secondary" | "on-color" | "text-link" | "danger" | "ghost";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export function Button({
  children,
  variant = "primary",
  size = "md",
  isLoading = false,
  leftIcon,
  rightIcon,
  className = "",
  disabled,
  ...props
}: ButtonProps) {
  const baseClasses =
    "inline-flex items-center justify-center font-medium transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-ink focus:ring-offset-2 focus:ring-offset-canvas disabled:opacity-50 disabled:pointer-events-none select-none";

  const sizeClasses = {
    sm: "h-[36px] px-3.5 text-xs rounded-sm gap-1.5",
    md: "h-[44px] px-5 text-sm rounded-md gap-2 min-h-[44px] min-w-[44px]", // Prompt: 44px high, padding 12x20, radius md
    lg: "h-[50px] px-6 text-base rounded-md gap-2.5",
  }[size];

  const variantClasses = {
    primary: "bg-ink text-on-primary hover:bg-neutral-800 active:scale-[0.99]",
    secondary: "bg-canvas text-ink border border-hairline hover:bg-surface-soft active:scale-[0.99]",
    "on-color": "bg-white text-ink hover:bg-surface-soft shadow-sm active:scale-[0.99]",
    "text-link": "bg-transparent text-ink underline underline-offset-4 hover:text-muted p-0 h-auto min-h-0 min-w-0 font-normal",
    danger: "bg-error text-white hover:bg-red-600 active:scale-[0.99]",
    ghost: "bg-transparent text-body hover:bg-surface-soft active:scale-[0.99]",
  }[variant];

  return (
    <button
      className={`${baseClasses} ${sizeClasses} ${variantClasses} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <svg
          className="animate-spin -ml-1 mr-2 h-4 w-4 text-current"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
      ) : (
        leftIcon && <span className="flex-shrink-0">{leftIcon}</span>
      )}
      <span>{children}</span>
      {!isLoading && rightIcon && <span className="flex-shrink-0">{rightIcon}</span>}
    </button>
  );
}
