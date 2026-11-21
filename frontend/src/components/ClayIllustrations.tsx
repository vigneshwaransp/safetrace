import React from "react";

export function HeroClayScene({ className = "" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 520 440"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`w-full h-auto drop-shadow-xl ${className}`}
      aria-label="Clay-style illustration of digital sanctuary and privacy guardian"
    >
      <defs>
        {/* Clay gradients with 3D diffuse highlights */}
        <linearGradient id="clay-mountain-bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#f5f0e0" />
          <stop offset="100%" stopColor="#ebe6d6" />
        </linearGradient>

        <linearGradient id="clay-mountain-teal" x1="20%" y1="0%" x2="80%" y2="100%">
          <stop offset="0%" stopColor="#2c5a5a" />
          <stop offset="100%" stopColor="#1a3a3a" />
        </linearGradient>

        <linearGradient id="clay-pink-orb" x1="30%" y1="20%" x2="90%" y2="90%">
          <stop offset="0%" stopColor="#ff85af" />
          <stop offset="70%" stopColor="#ff4d8b" />
          <stop offset="100%" stopColor="#d82b68" />
        </linearGradient>

        <linearGradient id="clay-lavender-torus" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#d4c7f7" />
          <stop offset="60%" stopColor="#b8a4ed" />
          <stop offset="100%" stopColor="#927cd4" />
        </linearGradient>

        <linearGradient id="clay-peach-pill" x1="10%" y1="0%" x2="90%" y2="100%">
          <stop offset="0%" stopColor="#ffd2b8" />
          <stop offset="50%" stopColor="#ffb084" />
          <stop offset="100%" stopColor="#e58752" />
        </linearGradient>

        <linearGradient id="clay-ochre-disc" x1="20%" y1="0%" x2="80%" y2="100%">
          <stop offset="0%" stopColor="#f3d17e" />
          <stop offset="70%" stopColor="#e8b94a" />
          <stop offset="100%" stopColor="#bd9027" />
        </linearGradient>

        <linearGradient id="clay-guardian-body" x1="20%" y1="10%" x2="80%" y2="100%">
          <stop offset="0%" stopColor="#ffffff" />
          <stop offset="60%" stopColor="#f0ede1" />
          <stop offset="100%" stopColor="#ded7c4" />
        </linearGradient>

        {/* Soft 3D clay shadow filters */}
        <filter id="clay-shadow" x="-10%" y="-10%" width="125%" height="130%" filterUnits="userSpaceOnUse">
          <feDropShadow dx="0" dy="12" stdDeviation="14" floodColor="#0a1a1a" floodOpacity="0.08" />
        </filter>

        <filter id="clay-shadow-soft" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur in="SourceAlpha" stdDeviation="8" />
          <feOffset dx="0" dy="10" result="offsetblur" />
          <feComponentTransfer>
            <feFuncA type="linear" slope="0.07" />
          </feComponentTransfer>
          <feMerge>
            <feMergeNode />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* Background Soft Clay Hills */}
      <path
        d="M20 380C60 310 140 290 200 330C260 370 330 330 390 350C440 366 480 340 510 370V430H20V380Z"
        fill="url(#clay-mountain-bg)"
      />
      <path
        d="M-10 400C80 340 180 370 260 340C340 310 420 360 530 320V440H-10V400Z"
        fill="url(#clay-mountain-teal)"
        opacity="0.9"
      />

      {/* Floating 3D Clay Shapes - Torus & Pills */}
      <g filter="url(#clay-shadow)">
        {/* Floating Lavender Torus / Ring */}
        <circle cx="100" cy="180" r="42" stroke="url(#clay-lavender-torus)" strokeWidth="22" strokeLinecap="round" />
        <ellipse cx="90" cy="165" rx="8" ry="4" fill="#ffffff" opacity="0.6" transform="rotate(-25 90 165)" />
      </g>

      <g filter="url(#clay-shadow)">
        {/* Floating Pink Clay Sphere */}
        <circle cx="420" cy="140" r="38" fill="url(#clay-pink-orb)" />
        <ellipse cx="408" cy="126" rx="12" ry="7" fill="#ffffff" opacity="0.45" transform="rotate(-30 408 126)" />
      </g>

      <g filter="url(#clay-shadow)">
        {/* Floating Ochre Disc */}
        <ellipse cx="370" cy="270" rx="46" ry="26" fill="url(#clay-ochre-disc)" />
        <ellipse cx="360" cy="262" rx="16" ry="5" fill="#ffffff" opacity="0.5" />
      </g>

      <g filter="url(#clay-shadow)">
        {/* Floating Peach Capsule / Pill */}
        <rect
          x="70"
          y="280"
          width="48"
          height="90"
          rx="24"
          fill="url(#clay-peach-pill)"
          transform="rotate(25 94 325)"
        />
        <ellipse cx="85" cy="300" rx="6" ry="14" fill="#ffffff" opacity="0.5" transform="rotate(25 85 300)" />
      </g>

      {/* Central Neutral Clay Guardian & Cryptographic Sanctuary */}
      <g filter="url(#clay-shadow)">
        {/* Guardian Body - Rounded Soft Clay Cone/Pill */}
        <path
          d="M210 240C210 185 240 165 270 165C300 165 330 185 330 240L342 340C342 355 330 365 315 365H225C210 365 198 355 198 340L210 240Z"
          fill="url(#clay-guardian-body)"
        />
        {/* Guardian Specular Highlight */}
        <path
          d="M235 220C240 185 255 175 270 175"
          stroke="#ffffff"
          strokeWidth="6"
          strokeLinecap="round"
          opacity="0.6"
        />

        {/* Guardian Head / Sphere */}
        <circle cx="270" cy="125" r="32" fill="url(#clay-guardian-body)" />
        <ellipse cx="260" cy="115" rx="9" ry="6" fill="#ffffff" opacity="0.7" transform="rotate(-20 260 115)" />

        {/* Tactile 3D Clay Shield (SafeTrace Symbol) */}
        <path
          d="M270 205C295 205 325 215 325 250C325 295 270 330 270 330C270 330 215 295 215 250C215 215 245 205 270 205Z"
          fill="url(#clay-pink-orb)"
          filter="url(#clay-shadow-soft)"
        />
        {/* Shield Inset Keyhole */}
        <circle cx="270" cy="250" r="10" fill="#ffffff" opacity="0.95" />
        <polygon points="266,252 274,252 277,272 263,272" fill="#ffffff" opacity="0.95" />
      </g>
    </svg>
  );
}

export function SecurityShieldClay({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
      <defs>
        <linearGradient id="shield-grad" x1="10%" y1="0%" x2="90%" y2="100%">
          <stop offset="0%" stopColor="#2c5a5a" />
          <stop offset="100%" stopColor="#1a3a3a" />
        </linearGradient>
        <linearGradient id="shield-pink" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#ff85af" />
          <stop offset="100%" stopColor="#ff4d8b" />
        </linearGradient>
      </defs>
      <circle cx="100" cy="100" r="85" fill="#faf5e8" />
      <path
        d="M100 35C125 35 155 45 155 85C155 130 100 165 100 165C100 165 45 130 45 85C45 45 75 35 100 35Z"
        fill="url(#shield-grad)"
      />
      <circle cx="100" cy="92" r="14" fill="url(#shield-pink)" />
      <path d="M96 95L93 120H107L104 95H96Z" fill="url(#shield-pink)" />
      <path d="M68 62C80 48 95 44 100 44" stroke="#ffffff" strokeWidth="4" strokeLinecap="round" opacity="0.4" />
    </svg>
  );
}

export function EmptyStateClay({ title, description }: { title: string; description: string }) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center bg-surface-soft/60 rounded-xl border border-hairline my-6">
      <div className="w-32 h-32 mb-4">
        <svg viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="80" cy="80" r="70" fill="#f5f0e0" />
          <rect x="45" y="65" width="70" height="50" rx="16" fill="#b8a4ed" />
          <path d="M40 68C40 55 52 48 80 48C108 48 120 55 120 68H40Z" fill="#ffb084" />
          <circle cx="80" cy="90" r="8" fill="#ffffff" opacity="0.9" />
          <circle cx="118" cy="42" r="5" fill="#ff4d8b" />
          <circle cx="42" cy="115" r="4" fill="#e8b94a" />
        </svg>
      </div>
      <h3 className="text-lg font-medium text-ink mb-1">{title}</h3>
      <p className="text-sm text-muted max-w-sm">{description}</p>
    </div>
  );
}
