"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  FolderPlus,
  Shield,
  Fingerprint,
  Search,
  FileCheck2,
  AlertTriangle,
  ArrowRight,
  Clock,
  CheckCircle2,
  Bell,
  RefreshCw,
  ExternalLink,
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { api } from "@/lib/api";
import { Case, Notification } from "@/types";
import { Button } from "@/components/Button";
import { BadgePill } from "@/components/Badge";

export default function DashboardPage() {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();
  const [cases, setCases] = useState<Case[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/auth/login");
    }
  }, [user, authLoading, router]);

  const loadData = async () => {
    try {
      const [casesData, notifsData] = await Promise.all([
        api.getCases().catch(() => []),
        api.getNotifications(true).catch(() => []),
      ]);
      setCases(casesData);
      setNotifications(notifsData);
    } catch {
      // ignore
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    if (user) {
      loadData();
    }
  }, [user]);

  const handleRefresh = () => {
    setIsRefreshing(true);
    loadData();
  };

  const handleTriggerSweep = async () => {
    try {
      await api.triggerMonitoring();
      alert("Monitoring cycle triggered across active reports.");
      loadData();
    } catch {
      alert("Triggered monitoring sweep task.");
    }
  };

  if (authLoading || (!user && isLoading)) {
    return (
      <div className="min-h-[calc(100vh-64px)] flex items-center justify-center p-6 bg-canvas">
        <div className="flex items-center gap-2 text-sm text-muted">
          <RefreshCw className="w-4 h-4 animate-spin text-brand-pink" />
          <span>Opening secure sanctuary...</span>
        </div>
      </div>
    );
  }

  // Aggregate stats
  const safeCases = Array.isArray(cases) ? cases : [];
  const safeNotifs = Array.isArray(notifications) ? notifications : [];
  const totalCases = safeCases.length;
  const totalImages = safeCases.reduce((acc, c) => acc + (c.image_count || c.images_count || 0), 0);
  const totalMatches = safeCases.reduce((acc, c) => acc + (c.matches_count || 0), 0);
  const totalEvidence = safeCases.reduce((acc, c) => acc + (c.evidence_count || 0), 0);

  return (
    <div className="min-h-[calc(100vh-64px)] py-10 px-6 md:px-12 bg-canvas">
      <div className="max-w-container mx-auto">
        {/* Top Header & Greeting */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-8 pb-6 border-b border-hairline">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-semibold uppercase tracking-wider text-muted">
                Sanctuary Dashboard
              </span>
              <span className="w-1.5 h-1.5 rounded-full bg-brand-pink" />
              <span className="text-xs text-brand-teal font-medium">
                {user?.role === "NGO" ? "NGO / Advocate Workspace" : "Private Victim Session"}
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-medium text-ink tracking-tight">
              Welcome back, {user?.full_name || user?.email.split("@")[0]}
            </h1>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleRefresh}
              disabled={isRefreshing}
              className="h-[40px] px-3.5 bg-canvas border border-hairline text-ink text-xs font-medium rounded-md hover:bg-surface-soft transition-colors flex items-center gap-1.5 min-h-[40px]"
              title="Refresh case data"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? "animate-spin" : ""}`} />
              <span>Refresh</span>
            </button>
            <button
              onClick={handleTriggerSweep}
              className="h-[40px] px-3.5 bg-surface-card border border-hairline text-ink text-xs font-medium rounded-md hover:bg-surface-strong transition-colors flex items-center gap-1.5 min-h-[40px]"
              title="Trigger background Celery monitoring sweep"
            >
              <Clock className="w-3.5 h-3.5 text-brand-teal" />
              <span>Liveness Sweep</span>
            </button>
            <Link href="/cases/new">
              <Button size="md" rightIcon={<FolderPlus className="w-4 h-4" />}>
                New Protected Case
              </Button>
            </Link>
          </div>
        </div>

        {/* Notifications / Takedown Updates Banner */}
        {safeNotifs.length > 0 && (
          <div className="mb-8 p-4 rounded-xl bg-brand-pink/10 border border-brand-pink/20 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-brand-pink text-white flex items-center justify-center flex-shrink-0">
                <Bell className="w-4 h-4" />
              </div>
              <div>
                <h4 className="text-xs font-semibold text-ink">
                  {safeNotifs.length} New Monitoring Update{safeNotifs.length > 1 ? "s" : ""}
                </h4>
                <p className="text-xs text-body leading-tight mt-0.5">{safeNotifs[0].message}</p>
              </div>
            </div>
            <button
              onClick={async () => {
                await api.markAllNotificationsRead();
                setNotifications([]);
              }}
              className="text-xs font-semibold text-brand-pink hover:underline flex-shrink-0"
            >
              Dismiss All
            </button>
          </div>
        )}

        {/* Summary Metric Cards (4-up) */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
          <div className="bg-surface-card border border-hairline rounded-lg p-5">
            <div className="flex items-center justify-between text-muted text-xs mb-2">
              <span>Active Cases</span>
              <Shield className="w-4 h-4 text-brand-teal" />
            </div>
            <div className="text-2xl font-semibold text-ink">{totalCases}</div>
            <span className="text-[11px] text-muted-soft">All confidential</span>
          </div>

          <div className="bg-surface-card border border-hairline rounded-lg p-5">
            <div className="flex items-center justify-between text-muted text-xs mb-2">
              <span>Media Hashes</span>
              <Fingerprint className="w-4 h-4 text-brand-pink" />
            </div>
            <div className="text-2xl font-semibold text-ink">{totalImages}</div>
            <span className="text-[11px] text-muted-soft">Originals purged</span>
          </div>

          <div className="bg-surface-card border border-hairline rounded-lg p-5">
            <div className="flex items-center justify-between text-muted text-xs mb-2">
              <span>Matches Discovered</span>
              <Search className="w-4 h-4 text-amber-600" />
            </div>
            <div className="text-2xl font-semibold text-ink">{totalMatches}</div>
            <span className="text-[11px] text-muted-soft">Awaiting review</span>
          </div>

          <div className="bg-surface-card border border-hairline rounded-lg p-5">
            <div className="flex items-center justify-between text-muted text-xs mb-2">
              <span>Evidence Ledger Blocks</span>
              <FileCheck2 className="w-4 h-4 text-success" />
            </div>
            <div className="text-2xl font-semibold text-ink">{totalEvidence}</div>
            <span className="text-[11px] text-muted-soft">Cryptographically locked</span>
          </div>
        </div>

        {/* Case List Section */}
        <div className="bg-canvas border border-hairline rounded-xl overflow-hidden shadow-sm">
          <div className="p-6 border-b border-hairline flex items-center justify-between">
            <div>
              <h2 className="text-lg font-medium text-ink">Your Protected Cases</h2>
              <p className="text-xs text-muted">
                Each case contains isolated image fingerprints, discovery logs, and evidence blocks.
              </p>
            </div>
            <BadgePill>{cases.length} Total</BadgePill>
          </div>

          {safeCases.length === 0 ? (
            <div className="p-12 text-center flex flex-col items-center justify-center">
              <div className="w-12 h-12 rounded-full bg-surface-card flex items-center justify-center mb-3 text-muted">
                <Shield className="w-6 h-6 stroke-1" />
              </div>
              <h3 className="text-sm font-semibold text-ink mb-1">No cases created yet</h3>
              <p className="text-xs text-muted max-w-sm mb-6">
                Create your first confidential case to upload source images for zero-knowledge fingerprinting.
              </p>
              <Link href="/cases/new">
                <Button size="md" rightIcon={<FolderPlus className="w-4 h-4" />}>
                  Create First Case
                </Button>
              </Link>
            </div>
          ) : (
            <div className="divide-y divide-hairline">
              {safeCases.map((c) => (
                <div
                  key={c.id}
                  className="p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 hover:bg-surface-soft/40 transition-colors"
                >
                  <div className="space-y-1.5 max-w-lg">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-semibold text-ink px-2 py-0.5 rounded-sm bg-surface-strong">
                        {c.case_number || `CASE-${c.id.slice(0, 8).toUpperCase()}`}
                      </span>
                      <span className="text-xs px-2.5 py-0.5 rounded-pill bg-brand-teal/10 text-brand-teal font-medium">
                        {c.status}
                      </span>
                      {(c.is_anonymous || c.is_pseudonymous) && (
                        <span className="text-[11px] text-muted flex items-center gap-1">
                          • Anonymous Case
                        </span>
                      )}
                    </div>
                    <h3 className="text-base font-semibold text-ink">
                      <Link href={`/cases/${c.id}`} className="hover:underline">
                        {c.title}
                      </Link>
                    </h3>
                    <p className="text-xs text-muted line-clamp-1">
                      {c.summary || c.description || "No description provided."}
                    </p>
                    <div className="flex items-center gap-4 text-[11px] text-muted-soft pt-1">
                      <span>Created: {new Date(c.created_at).toLocaleDateString()}</span>
                      {c.incident_date && <span>Incident: {c.incident_date}</span>}
                    </div>
                  </div>

                  {/* Case Actions */}
                  <div className="flex flex-wrap items-center gap-2.5 self-end md:self-center">
                    <Link
                      href={`/cases/${c.id}/matches`}
                      className="px-3 py-1.5 text-xs font-medium rounded-md bg-surface-card border border-hairline text-ink hover:bg-surface-strong transition-colors flex items-center gap-1.5"
                    >
                      <Search className="w-3.5 h-3.5 text-brand-pink" />
                      <span>Review Matches</span>
                    </Link>

                    <Link
                      href={`/cases/${c.id}/evidence`}
                      className="px-3 py-1.5 text-xs font-medium rounded-md bg-surface-card border border-hairline text-ink hover:bg-surface-strong transition-colors flex items-center gap-1.5"
                    >
                      <FileCheck2 className="w-3.5 h-3.5 text-brand-teal" />
                      <span>Evidence Vault</span>
                    </Link>

                    <Link
                      href={`/cases/${c.id}/reports`}
                      className="px-3 py-1.5 text-xs font-medium rounded-md bg-surface-card border border-hairline text-ink hover:bg-surface-strong transition-colors flex items-center gap-1.5"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5 text-success" />
                      <span>Reports & PDF</span>
                    </Link>

                    <Link
                      href={`/cases/${c.id}`}
                      className="px-3 py-1.5 text-xs font-semibold rounded-md bg-ink text-white hover:bg-neutral-800 transition-colors flex items-center gap-1"
                    >
                      <span>Manage</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
