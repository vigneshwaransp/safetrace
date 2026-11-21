"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  Search,
  ShieldCheck,
  Check,
  X,
  HelpCircle,
  ExternalLink,
  ArrowLeft,
  Clock,
  Layers,
  Sparkles,
  AlertTriangle,
  RefreshCw,
  FileCheck2,
} from "lucide-react";
import { api } from "@/lib/api";
import { Match, MatchStatus } from "@/types";
import { ConfidenceBadge, BadgePill } from "@/components/Badge";
import { ThumbnailBlur } from "@/components/ThumbnailBlur";
import { Button } from "@/components/Button";

export default function MatchReviewPage() {
  const params = useParams();
  const caseId = params.id as string;

  const [matches, setMatches] = useState<Match[]>([]);
  const [filter, setFilter] = useState<string>("ALL");
  const [isLoading, setIsLoading] = useState(true);
  const [processingId, setProcessingId] = useState<string | null>(null);
  const [notification, setNotification] = useState<string | null>(null);

  const loadMatches = async () => {
    try {
      const data = await api.getMatches(caseId);
      setMatches(data);
    } catch {
      // If none yet or demo
      setMatches([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadMatches();
  }, [caseId]);

  const handleReview = async (matchId: string, status: "CONFIRMED" | "REJECTED" | "UNSURE") => {
    setProcessingId(matchId);
    try {
      const updated = await api.reviewMatch(matchId, status);
      setMatches((prev) => prev.map((m) => (m.id === matchId ? updated : m)));
      if (status === "CONFIRMED") {
        setNotification(
          "Match confirmed! Added to your tamper-evident Cryptographic Evidence Vault with block sequence."
        );
      } else if (status === "REJECTED") {
        setNotification("Match marked as false positive.");
      } else {
        setNotification("Marked as unsure for advocate review.");
      }
    } catch (err: any) {
      alert(err.message || "Review action failed");
    } finally {
      setProcessingId(null);
    }
  };

  const filteredMatches = matches.filter((m) => {
    if (filter === "ALL") return true;
    return m.status === filter;
  });

  const pendingCount = matches.filter((m) => m.status === "PENDING_REVIEW").length;
  const confirmedCount = matches.filter((m) => m.status === "CONFIRMED").length;

  return (
    <div className="min-h-[calc(100vh-64px)] py-10 px-6 md:px-12 bg-canvas">
      <div className="max-w-container mx-auto">
        {/* Navigation Breadcrumb */}
        <div className="flex items-center justify-between mb-6">
          <Link
            href={`/cases/${caseId}`}
            className="inline-flex items-center gap-1.5 text-xs font-medium text-muted hover:text-ink transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Case Overview</span>
          </Link>
          <div className="flex items-center gap-3">
            <Link
              href={`/cases/${caseId}/evidence`}
              className="text-xs font-semibold text-brand-teal hover:underline flex items-center gap-1"
            >
              <FileCheck2 className="w-3.5 h-3.5" />
              <span>View Evidence Vault ({confirmedCount}) →</span>
            </Link>
          </div>
        </div>

        {/* Header */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-6 mb-8 border-b border-hairline">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="text-xs font-semibold uppercase tracking-wider text-muted">
                Human-in-the-Loop Review
              </span>
              <span className="w-1.5 h-1.5 rounded-full bg-brand-pink" />
              <span className="text-xs text-brand-teal font-medium">Ranked Similarity</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-medium text-ink tracking-tight">
              Discovered Matches & Re-Uploads
            </h1>
            <p className="text-xs text-muted max-w-2xl mt-1">
              Confirming a match permanently commits it into the tamper-evident cryptographic hash chain as verifiable
              legal evidence.
            </p>
          </div>

          <button
            onClick={() => {
              setIsLoading(true);
              loadMatches();
            }}
            className="h-[38px] px-3.5 bg-surface-card border border-hairline text-ink text-xs font-medium rounded-md hover:bg-surface-strong transition-colors flex items-center gap-1.5"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? "animate-spin" : ""}`} />
            <span>Refresh Scan</span>
          </button>
        </div>

        {/* Notification Banner */}
        {notification && (
          <div className="mb-6 p-4 rounded-xl bg-surface-card border border-brand-pink/30 flex items-center justify-between gap-3 text-xs text-ink">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-brand-pink flex-shrink-0" />
              <span className="font-medium">{notification}</span>
            </div>
            <button
              onClick={() => setNotification(null)}
              className="text-muted hover:text-ink font-semibold"
            >
              ✕
            </button>
          </div>
        )}

        {/* Filter Pills */}
        <div className="flex flex-wrap items-center gap-2 mb-8">
          {[
            { id: "ALL", label: `All (${matches.length})` },
            { id: "PENDING_REVIEW", label: `Pending Review (${pendingCount})` },
            { id: "CONFIRMED", label: `Confirmed Evidence (${confirmedCount})` },
            { id: "REJECTED", label: "Rejected False Positives" },
            { id: "UNSURE", label: "Unsure" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setFilter(tab.id)}
              className={`px-3.5 py-1.5 rounded-pill text-xs font-medium transition-colors border ${
                filter === tab.id
                  ? "bg-surface-strong border-ink text-ink font-semibold"
                  : "bg-canvas border-hairline text-muted hover:bg-surface-soft"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Matches Grid */}
        {isLoading ? (
          <div className="p-16 text-center text-sm text-muted flex items-center justify-center gap-2">
            <RefreshCw className="w-4 h-4 animate-spin text-brand-pink" />
            <span>Loading candidates...</span>
          </div>
        ) : filteredMatches.length === 0 ? (
          <div className="bg-canvas border border-hairline rounded-xl p-16 text-center flex flex-col items-center justify-center">
            <Search className="w-10 h-10 text-muted-soft mb-3 stroke-1" />
            <h3 className="text-base font-semibold text-ink mb-1">No candidate matches in this filter</h3>
            <p className="text-xs text-muted max-w-sm mb-6">
              Run a discovery sweep from the Case Overview page or submit specific candidate URLs directly.
            </p>
            <Link href={`/cases/${caseId}`}>
              <Button size="sm">Go to Case Overview</Button>
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredMatches.map((m) => {
              const isProcessing = processingId === m.id;
              return (
                <div
                  key={m.id}
                  className="bg-canvas border border-hairline rounded-xl overflow-hidden shadow-sm flex flex-col justify-between"
                >
                  <div>
                    {/* Trauma-Informed Blurred Media Preview */}
                    <div className="p-4 pb-0">
                      <ThumbnailBlur src={m.thumbnail_url} aspectRatio="video" />
                    </div>

                    {/* Match Metadata */}
                    <div className="p-5 space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-xs px-2.5 py-0.5 rounded-pill bg-surface-strong text-ink uppercase tracking-wider">
                          {m.platform}
                        </span>
                        <ConfidenceBadge confidence={m.confidence} />
                      </div>

                      <div>
                        <div className="flex items-baseline justify-between mb-1">
                          <span className="text-xs text-muted">Similarity Score:</span>
                          <span className="text-lg font-bold text-ink">
                            {m.similarity_score.toFixed(1)}%
                          </span>
                        </div>
                        {/* Progress Bar */}
                        <div className="w-full h-1.5 bg-surface-card rounded-full overflow-hidden">
                          <div
                            className={`h-full ${
                              m.similarity_score >= 80
                                ? "bg-brand-pink"
                                : m.similarity_score >= 60
                                ? "bg-amber-500"
                                : "bg-neutral-400"
                            }`}
                            style={{ width: `${Math.min(100, m.similarity_score)}%` }}
                          />
                        </div>
                      </div>

                      {/* Source URL & Poster Handle */}
                      <div className="text-xs space-y-1 pt-1">
                        <div className="flex items-center justify-between text-muted">
                          <span>Poster / Handle:</span>
                          <span className="font-mono text-ink">{m.author_handle || "@unknown"}</span>
                        </div>
                        <div className="truncate">
                          <a
                            href={m.source_url}
                            target="_blank"
                            rel="noreferrer"
                            className="text-[11px] text-brand-teal hover:underline flex items-center gap-1 truncate"
                          >
                            <span className="truncate">{m.source_url}</span>
                            <ExternalLink className="w-3 h-3 flex-shrink-0" />
                          </a>
                        </div>
                      </div>

                      {/* Matching Reasons */}
                      {m.matching_reasons && m.matching_reasons.length > 0 && (
                        <div className="bg-surface-card rounded-md p-2.5 border border-hairline text-[11px] text-body space-y-1">
                          <span className="font-medium text-ink block text-[10px] uppercase tracking-wider">
                            Detection Analysis:
                          </span>
                          {m.matching_reasons.map((r, idx) => (
                            <div key={idx} className="flex items-center gap-1.5 text-muted">
                              <span className="w-1 h-1 rounded-full bg-brand-pink" />
                              <span>{r}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Review Actions Footer */}
                  <div className="p-4 bg-surface-soft/60 border-t border-hairline">
                    {m.status === "CONFIRMED" ? (
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-green-800 font-semibold flex items-center gap-1 bg-success/15 px-3 py-1 rounded-pill border border-success/30">
                          <Check className="w-3.5 h-3.5" />
                          <span>Confirmed in Vault</span>
                        </span>
                        <Link
                          href={`/cases/${caseId}/evidence`}
                          className="text-xs font-semibold text-brand-teal hover:underline"
                        >
                          View Block →
                        </Link>
                      </div>
                    ) : m.status === "REJECTED" ? (
                      <div className="flex items-center justify-between text-xs text-muted">
                        <span>Rejected (False Positive)</span>
                        <button
                          onClick={() => handleReview(m.id, "CONFIRMED")}
                          className="text-[11px] font-semibold text-ink hover:underline"
                        >
                          Reopen & Confirm
                        </button>
                      </div>
                    ) : (
                      <div className="grid grid-cols-3 gap-2">
                        <button
                          onClick={() => handleReview(m.id, "CONFIRMED")}
                          disabled={isProcessing}
                          className="h-[38px] px-2 bg-ink text-white font-semibold text-xs rounded-md hover:bg-neutral-800 transition-colors flex items-center justify-center gap-1 min-h-[38px]"
                          title="Confirm this is a non-consensual violation"
                        >
                          <Check className="w-3.5 h-3.5" />
                          <span>Confirm</span>
                        </button>
                        <button
                          onClick={() => handleReview(m.id, "REJECTED")}
                          disabled={isProcessing}
                          className="h-[38px] px-2 bg-canvas border border-hairline text-ink font-medium text-xs rounded-md hover:bg-surface-card transition-colors flex items-center justify-center gap-1 min-h-[38px]"
                          title="Reject as false positive"
                        >
                          <X className="w-3.5 h-3.5 text-muted" />
                          <span>Reject</span>
                        </button>
                        <button
                          onClick={() => handleReview(m.id, "UNSURE")}
                          disabled={isProcessing}
                          className="h-[38px] px-2 bg-surface-card border border-hairline text-muted font-medium text-xs rounded-md hover:bg-surface-strong transition-colors flex items-center justify-center gap-1 min-h-[38px]"
                          title="Flag as unsure"
                        >
                          <HelpCircle className="w-3.5 h-3.5" />
                          <span>Unsure</span>
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
