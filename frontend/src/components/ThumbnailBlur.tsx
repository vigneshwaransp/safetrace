"use client";

import React, { useState } from "react";
import { Eye, EyeOff, ShieldAlert } from "lucide-react";

interface ThumbnailBlurProps {
  src?: string | null;
  alt?: string;
  className?: string;
  aspectRatio?: "square" | "video" | "auto";
}

export function ThumbnailBlur({
  src,
  alt = "Candidate media thumbnail",
  className = "",
  aspectRatio = "video",
}: ThumbnailBlurProps) {
  const [isRevealed, setIsRevealed] = useState(false);

  const aspectClass = {
    square: "aspect-square",
    video: "aspect-video",
    auto: "h-48",
  }[aspectRatio];

  if (!src) {
    return (
      <div
        className={`w-full ${aspectClass} rounded-md bg-surface-card border border-hairline flex flex-col items-center justify-center p-4 text-center text-muted ${className}`}
      >
        <ShieldAlert className="w-8 h-8 text-muted-soft mb-2 stroke-1" />
        <span className="text-xs">No media preview available</span>
      </div>
    );
  }

  return (
    <div
      className={`relative overflow-hidden rounded-md border border-hairline bg-surface-card select-none ${aspectClass} ${className}`}
    >
      {/* Background Image with Trauma-Informed Blur Filter */}
      <img
        src={src}
        alt={alt}
        className={`w-full h-full object-cover transition-all duration-300 ${
          isRevealed ? "filter-none" : "filter blur-2xl scale-110 opacity-60"
        }`}
      />

      {/* Overlay Shield with Click-to-Reveal */}
      {!isRevealed ? (
        <div className="absolute inset-0 bg-ink/40 backdrop-blur-sm flex flex-col items-center justify-center p-3 text-center transition-opacity">
          <button
            type="button"
            onClick={() => setIsRevealed(true)}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-canvas/95 hover:bg-canvas text-ink text-xs font-medium rounded-pill shadow-sm transition-transform active:scale-95"
          >
            <Eye className="w-3.5 h-3.5" />
            <span>Click to Reveal</span>
          </button>
          <span className="text-[11px] text-surface-soft mt-1.5 opacity-90 max-w-[200px] leading-tight">
            Blurred to prevent unintended exposure
          </span>
        </div>
      ) : (
        <div className="absolute top-2 right-2">
          <button
            type="button"
            onClick={() => setIsRevealed(false)}
            className="inline-flex items-center gap-1 px-2.5 py-1 bg-ink/80 hover:bg-ink text-white text-xs font-medium rounded-pill backdrop-blur-sm transition-all"
            title="Blur image again"
          >
            <EyeOff className="w-3 h-3" />
            <span>Hide</span>
          </button>
        </div>
      )}
    </div>
  );
}
