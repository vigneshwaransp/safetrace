"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  FolderPlus,
  Shield,
  Lock,
  ArrowRight,
  ArrowLeft,
  Check,
  AlertCircle,
  Globe,
  Info,
} from "lucide-react";
import { api } from "@/lib/api";
import { Button } from "@/components/Button";

const PLATFORMS = [
  { id: "META", label: "Instagram & Facebook (Meta)" },
  { id: "X_TWITTER", label: "X (Twitter)" },
  { id: "REDDIT", label: "Reddit" },
  { id: "YOUTUBE", label: "YouTube Shorts / Video" },
  { id: "BLUESKY", label: "Bluesky (AT Protocol)" },
  { id: "WEB", label: "Open Web / Image Hosts" },
];

export default function NewCasePage() {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [incidentDate, setIncidentDate] = useState("");
  const [summary, setSummary] = useState("");
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(["META", "REDDIT", "X_TWITTER"]);
  const [targetUrlsRaw, setTargetUrlsRaw] = useState("");
  const [isAnonymous, setIsAnonymous] = useState(true);
  const [retainEncryptedFiles, setRetainEncryptedFiles] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const togglePlatform = (p: string) => {
    if (selectedPlatforms.includes(p)) {
      setSelectedPlatforms(selectedPlatforms.filter((item) => item !== p));
    } else {
      setSelectedPlatforms([...selectedPlatforms, p]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      setError("Please provide a title for this case.");
      return;
    }
    setError(null);
    setIsLoading(true);

    try {
      const urls = targetUrlsRaw
        .split("\n")
        .map((u) => u.trim())
        .filter((u) => u.length > 0);

      const created = await api.createCase({
        title,
        incident_date: incidentDate || undefined,
        summary: summary || undefined,
        suspected_platforms: selectedPlatforms,
        target_urls: urls,
        is_anonymous: isAnonymous,
        retain_encrypted_files: retainEncryptedFiles,
      });

      router.push(`/cases/${created.id}`);
    } catch (err: any) {
      setError(err.message || "Failed to create case. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] py-10 px-6 md:px-12 bg-canvas">
      <div className="max-w-3xl mx-auto">
        {/* Back Link */}
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-1.5 text-xs font-medium text-muted hover:text-ink mb-6 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Dashboard</span>
        </Link>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-semibold uppercase tracking-wider text-muted">
              Confidential Intake
            </span>
            <span className="w-1.5 h-1.5 rounded-full bg-brand-pink" />
            <span className="text-xs text-brand-teal font-medium">Safe Haven</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-medium text-ink tracking-tight mb-2">
            Create a New Protected Case
          </h1>
          <p className="text-sm text-body">
            Set up an isolated workspace for your incident. You will be able to upload source media for
            zero-knowledge fingerprinting in the next step.
          </p>
        </div>

        {/* Intake Form */}
        <div className="bg-canvas border border-hairline rounded-xl p-8 shadow-sm">
          {error && (
            <div className="mb-6 p-3.5 rounded-md bg-error/10 border border-error/20 flex items-start gap-2.5 text-xs text-error">
              <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Case Title */}
            <div>
              <label className="block text-xs font-semibold text-ink uppercase tracking-wider mb-2">
                Case Title *
              </label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Unauthorized circulation on Reddit & Telegram channels"
                className="w-full h-[44px] px-4 rounded-md bg-canvas border border-hairline text-ink text-sm focus:outline-none focus:border-ink transition-colors"
              />
            </div>

            {/* Incident Date */}
            <div>
              <label className="block text-xs font-semibold text-ink uppercase tracking-wider mb-2">
                Estimated Date of Discovery / Incident (Optional)
              </label>
              <input
                type="date"
                value={incidentDate}
                onChange={(e) => setIncidentDate(e.target.value)}
                className="w-full h-[44px] px-4 rounded-md bg-canvas border border-hairline text-ink text-sm focus:outline-none focus:border-ink transition-colors"
              />
            </div>

            {/* Summary */}
            <div>
              <label className="block text-xs font-semibold text-ink uppercase tracking-wider mb-2">
                Incident Summary / Context (Optional)
              </label>
              <textarea
                rows={3}
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
                placeholder="Briefly describe what happened, any specific threats, or where you believe the content originated. This will assist when generating legal notices."
                className="w-full p-4 rounded-md bg-canvas border border-hairline text-ink text-sm focus:outline-none focus:border-ink transition-colors resize-none"
              />
            </div>

            {/* Suspected Platforms Multi-Select */}
            <div>
              <label className="block text-xs font-semibold text-ink uppercase tracking-wider mb-2">
                Suspected Platforms to Scan
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {PLATFORMS.map((plat) => {
                  const isChecked = selectedPlatforms.includes(plat.id);
                  return (
                    <button
                      key={plat.id}
                      type="button"
                      onClick={() => togglePlatform(plat.id)}
                      className={`h-[42px] px-3.5 text-xs font-medium rounded-md border flex items-center justify-between transition-colors ${
                        isChecked
                          ? "bg-surface-card border-ink text-ink font-semibold"
                          : "bg-canvas border-hairline text-body hover:bg-surface-soft"
                      }`}
                    >
                      <span>{plat.label}</span>
                      {isChecked && <Check className="w-4 h-4 text-brand-pink" />}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Target URLs to Check Immediately */}
            <div>
              <label className="block text-xs font-semibold text-ink uppercase tracking-wider mb-2">
                Known Post or Profile URLs (One per line)
              </label>
              <textarea
                rows={3}
                value={targetUrlsRaw}
                onChange={(e) => setTargetUrlsRaw(e.target.value)}
                placeholder="https://reddit.com/r/...&#10;https://x.com/.../status/..."
                className="w-full p-4 rounded-md bg-canvas border border-hairline text-ink text-sm focus:outline-none focus:border-ink transition-colors font-mono text-xs resize-none"
              />
              <span className="text-[11px] text-muted-soft mt-1 block">
                SafeTrace will automatically fingerprint media from these specific URLs during discovery.
              </span>
            </div>

            {/* Privacy & Zero-Knowledge Toggles */}
            <div className="pt-4 border-t border-hairline space-y-4">
              <span className="block text-xs font-semibold text-ink uppercase tracking-wider">
                Cryptographic & Privacy Safeguards
              </span>

              {/* Zero-Storage Guarantee */}
              <div className="p-4 rounded-lg bg-surface-card border border-hairline flex items-start justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-1.5 text-xs font-semibold text-ink">
                    <Shield className="w-4 h-4 text-brand-teal" />
                    <span>Zero-Storage Guarantee (Purge Raw Media After Hashing)</span>
                    <span className="text-[10px] bg-brand-teal text-white px-2 py-0.2 rounded-pill font-normal">
                      Recommended
                    </span>
                  </div>
                  <p className="text-[11px] text-muted leading-relaxed">
                    Once PDQ and perceptual fingerprints are calculated, your original files are permanently deleted
                    from our servers. Only cryptographic mathematical vectors are preserved.
                  </p>
                </div>
                <input
                  type="checkbox"
                  checked={!retainEncryptedFiles}
                  onChange={(e) => setRetainEncryptedFiles(!e.target.checked)}
                  className="w-4 h-4 mt-1 accent-ink rounded cursor-pointer"
                />
              </div>

              {/* Pseudonymity */}
              <div className="p-4 rounded-lg bg-surface-card border border-hairline flex items-start justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-1.5 text-xs font-semibold text-ink">
                    <Lock className="w-4 h-4 text-brand-pink" />
                    <span>Anonymous Case Masking</span>
                  </div>
                  <p className="text-[11px] text-muted leading-relaxed">
                    Masks all user-identifiable names in discovery logs and generated draft filings until you choose
                    to disclose your identity in court submissions.
                  </p>
                </div>
                <input
                  type="checkbox"
                  checked={isAnonymous}
                  onChange={(e) => setIsAnonymous(e.target.checked)}
                  className="w-4 h-4 mt-1 accent-ink rounded cursor-pointer"
                />
              </div>
            </div>

            <Button
              type="submit"
              size="lg"
              className="w-full"
              isLoading={isLoading}
              rightIcon={<ArrowRight className="w-4 h-4" />}
            >
              Initialize Protected Case
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
