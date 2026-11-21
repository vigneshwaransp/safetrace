import React from "react";
import { MatchConfidence, ReportStatus } from "@/types";

export function ConfidenceBadge({ confidence }: { confidence: MatchConfidence }) {
  const styles = {
    HIGH: "bg-brand-pink/15 text-brand-pink border border-brand-pink/30 font-semibold",
    MEDIUM: "bg-warning/15 text-amber-700 border border-warning/30 font-medium",
    LOW: "bg-surface-strong text-muted border border-hairline font-medium",
    NONE: "bg-surface-soft text-muted-soft border border-hairline font-normal",
  }[confidence];

  const labels = {
    HIGH: "High Confidence",
    MEDIUM: "Medium Confidence",
    LOW: "Low Similarity",
    NONE: "No Match",
  }[confidence];

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-pill text-xs tracking-tight ${styles}`}>
      <span className="w-1.5 h-1.5 rounded-full mr-1.5 bg-current opacity-80" />
      {labels}
    </span>
  );
}

export function StatusBadge({ status }: { status: ReportStatus }) {
  const config = {
    DRAFT: {
      bg: "bg-surface-card text-body border-hairline",
      label: "Draft",
    },
    SUBMITTED: {
      bg: "bg-blue-50 text-blue-700 border-blue-200",
      label: "Submitted",
    },
    ACKNOWLEDGED: {
      bg: "bg-purple-50 text-purple-700 border-purple-200",
      label: "Acknowledged",
    },
    REMOVED: {
      bg: "bg-success/15 text-green-800 border-success/30 font-medium",
      label: "Removed / Offline",
    },
    REJECTED: {
      bg: "bg-error/15 text-error border-error/30",
      label: "Rejected by Platform",
    },
    REAPPEARED: {
      bg: "bg-brand-coral/20 text-brand-coral border-brand-coral/40 font-semibold animate-pulse",
      label: "Reappeared!",
    },
  }[status] || { bg: "bg-surface-card text-muted", label: status };

  return (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-pill text-xs border ${config.bg}`}>
      {config.label}
    </span>
  );
}

export function BadgePill({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <span
      className={`inline-flex items-center px-3 py-1 rounded-pill text-xs font-medium bg-surface-card text-body border border-hairline ${className}`}
    >
      {children}
    </span>
  );
}
