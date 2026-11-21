import React from "react";

export type FeatureCardColor = "pink" | "teal" | "lavender" | "peach" | "ochre" | "cream";

export function FeatureCard({
  color = "cream",
  title,
  description,
  icon,
  badge,
  className = "",
  children,
}: {
  color?: FeatureCardColor;
  title: string;
  description: string;
  icon?: React.ReactNode;
  badge?: string;
  className?: string;
  children?: React.ReactNode;
}) {
  const colorStyles: Record<FeatureCardColor, { bg: string; text: string; desc: string; badge: string }> = {
    pink: {
      bg: "bg-brand-pink",
      text: "text-white",
      desc: "text-white/90",
      badge: "bg-white/20 text-white border-white/30",
    },
    teal: {
      bg: "bg-brand-teal",
      text: "text-white",
      desc: "text-white/80",
      badge: "bg-white/15 text-white border-white/20",
    },
    lavender: {
      bg: "bg-brand-lavender",
      text: "text-ink",
      desc: "text-body",
      badge: "bg-ink/10 text-ink border-ink/20",
    },
    peach: {
      bg: "bg-brand-peach",
      text: "text-ink",
      desc: "text-body",
      badge: "bg-ink/10 text-ink border-ink/20",
    },
    ochre: {
      bg: "bg-brand-ochre",
      text: "text-ink",
      desc: "text-body",
      badge: "bg-ink/10 text-ink border-ink/20",
    },
    cream: {
      bg: "bg-surface-card border border-hairline",
      text: "text-ink",
      desc: "text-body",
      badge: "bg-surface-strong text-muted border-hairline",
    },
  };

  const current = colorStyles[color];

  return (
    <div
      className={`rounded-xl p-8 flex flex-col justify-between transition-all duration-200 select-none ${current.bg} ${className}`}
    >
      <div>
        <div className="flex items-center justify-between mb-6">
          {icon && <div className="text-current opacity-90">{icon}</div>}
          {badge && (
            <span className={`text-xs px-2.5 py-1 rounded-pill font-medium border ${current.badge}`}>{badge}</span>
          )}
        </div>
        <h3 className={`text-xl font-medium mb-3 tracking-tight ${current.text}`}>{title}</h3>
        <p className={`text-sm leading-relaxed ${current.desc}`}>{description}</p>
      </div>
      {children && <div className="mt-6 pt-4 border-t border-black/10">{children}</div>}
    </div>
  );
}

export function ProductMockupCard({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={`bg-canvas border border-hairline rounded-lg p-6 shadow-sm ${className}`}>
      {children}
    </div>
  );
}

export function TestimonialCard({
  quote,
  author,
  role,
  avatar,
  className = "",
}: {
  quote: string;
  author: string;
  role: string;
  avatar?: string;
  className?: string;
}) {
  return (
    <div className={`bg-surface-card rounded-lg p-6 flex flex-col justify-between border border-hairline ${className}`}>
      <p className="text-body text-sm italic leading-relaxed mb-6">"{quote}"</p>
      <div className="flex items-center gap-3">
        {avatar ? (
          <img src={avatar} alt={author} className="w-10 h-10 rounded-full object-cover" />
        ) : (
          <div className="w-10 h-10 rounded-full bg-brand-lavender text-ink font-semibold flex items-center justify-center text-sm">
            {author.charAt(0)}
          </div>
        )}
        <div>
          <h4 className="text-xs font-semibold text-ink">{author}</h4>
          <p className="text-[11px] text-muted">{role}</p>
        </div>
      </div>
    </div>
  );
}

export function PricingTierCard({
  title,
  price,
  billingPeriod = "/month",
  description,
  features,
  isFeatured = false,
  ctaText = "Get Started",
  ctaHref = "/auth/register",
  className = "",
}: {
  title: string;
  price: string;
  billingPeriod?: string;
  description: string;
  features: string[];
  isFeatured?: boolean;
  ctaText?: string;
  ctaHref?: string;
  className?: string;
}) {
  if (isFeatured) {
    return (
      <div
        className={`bg-brand-teal text-white rounded-lg p-8 flex flex-col justify-between shadow-md relative overflow-hidden ${className}`}
      >
        <div className="absolute top-4 right-4 bg-brand-pink text-white text-[11px] font-semibold px-2.5 py-0.5 rounded-pill uppercase tracking-wider">
          Recommended
        </div>
        <div>
          <h3 className="text-xl font-medium mb-2">{title}</h3>
          <p className="text-white/80 text-xs mb-6 min-h-[32px]">{description}</p>
          <div className="flex items-baseline mb-6">
            <span className="text-4xl font-semibold tracking-tight">{price}</span>
            <span className="text-xs text-white/70 ml-1.5">{billingPeriod}</span>
          </div>
          <ul className="space-y-3 mb-8 text-xs text-white/90">
            {features.map((feat, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-brand-pink font-bold">✓</span>
                <span>{feat}</span>
              </li>
            ))}
          </ul>
        </div>
        <a
          href={ctaHref}
          className="w-full h-[44px] bg-white text-brand-teal font-semibold text-sm rounded-md hover:bg-surface-soft transition-colors min-h-[44px] flex items-center justify-center text-center"
        >
          {ctaText}
        </a>
      </div>
    );
  }

  return (
    <div
      className={`bg-canvas border border-hairline rounded-lg p-8 flex flex-col justify-between ${className}`}
    >
      <div>
        <h3 className="text-xl font-medium text-ink mb-2">{title}</h3>
        <p className="text-muted text-xs mb-6 min-h-[32px]">{description}</p>
        <div className="flex items-baseline mb-6">
          <span className="text-4xl font-semibold text-ink tracking-tight">{price}</span>
          <span className="text-xs text-muted ml-1.5">{billingPeriod}</span>
        </div>
        <ul className="space-y-3 mb-8 text-xs text-body">
          {features.map((feat, idx) => (
            <li key={idx} className="flex items-start gap-2">
              <span className="text-success font-bold">✓</span>
              <span>{feat}</span>
            </li>
          ))}
        </ul>
      </div>
      <a
        href={ctaHref}
        className="w-full h-[44px] bg-surface-card border border-hairline text-ink font-medium text-sm rounded-md hover:bg-surface-strong transition-colors min-h-[44px] flex items-center justify-center text-center"
      >
        {ctaText}
      </a>
    </div>
  );
}
