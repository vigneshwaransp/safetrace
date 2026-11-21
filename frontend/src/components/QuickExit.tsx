"use client";

import React, { useEffect, useState } from "react";
import { LogOut } from "lucide-react";

export function QuickExit({ className = "" }: { className?: string }) {
  const [pressedOnce, setPressedOnce] = useState(false);

  const handleQuickExit = () => {
    // Overwrite local sensitive session
    try {
      localStorage.removeItem("safetrace_token");
      sessionStorage.clear();
    } catch {
      // ignore
    }
    // Replace window location immediately to prevent browser "back" navigation showing case data
    window.location.replace("https://weather.com/");
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        if (pressedOnce) {
          handleQuickExit();
        } else {
          setPressedOnce(true);
          const timer = setTimeout(() => setPressedOnce(false), 2000);
          return () => clearTimeout(timer);
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [pressedOnce]);

  return (
    <button
      onClick={handleQuickExit}
      title="Press ESC twice or click to instantly leave this page and open Weather"
      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-pill bg-error text-white font-medium text-xs hover:bg-red-600 transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-error focus:ring-offset-2 focus:ring-offset-canvas ${className}`}
      aria-label="Quick Exit - leave site immediately"
    >
      <LogOut className="w-3.5 h-3.5" />
      <span>{pressedOnce ? "Press Esc again to Exit" : "Quick Exit (Esc)"}</span>
    </button>
  );
}
