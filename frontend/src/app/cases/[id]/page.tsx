"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import {
  Shield,
  Fingerprint,
  UploadCloud,
  Trash2,
  Search,
  FileCheck2,
  CheckCircle2,
  ArrowRight,
  AlertCircle,
  Lock,
  Layers,
  Sparkles,
  Link as LinkIcon,
  RefreshCw,
} from "lucide-react";
import { api } from "@/lib/api";
import { Case, CaseImage } from "@/types";
import { Button } from "@/components/Button";
import { BadgePill } from "@/components/Badge";

export default function CaseDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const caseId = params.id as string;

  const [caseData, setCaseData] = useState<Case | null>(null);
  const [images, setImages] = useState<CaseImage[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [isDiscovering, setIsDiscovering] = useState(false);
  const [retainEncrypted, setRetainEncrypted] = useState(false);
  const [manualUrl, setManualUrl] = useState("");
  const [isScanningUrl, setIsScanningUrl] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const loadCase = async () => {
    try {
      const data = await api.getCase(caseId);
      setCaseData(data);
      // Backend returns images array attached or we get matches
    } catch {
      // ignore
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadCase();
  }, [caseId]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    setIsUploading(true);
    setStatusMessage(null);

    try {
      const uploaded = await api.uploadCaseImage(caseId, file, retainEncrypted);
      setImages((prev) => [uploaded, ...prev]);
      setStatusMessage(
        `Calculated perceptual fingerprints for ${file.name}. ${
          uploaded.is_original_deleted ? "Original media permanently purged." : "Encrypted at rest with AES-256."
        }`
      );
      loadCase();
    } catch (err: any) {
      alert(err.message || "Upload failed");
    } finally {
      setIsUploading(false);
    }
  };

  const handlePurge = async (imageId: string) => {
    if (!confirm("Are you sure? This permanently deletes the raw image file, retaining only cryptographic hashes."))
      return;
    try {
      await api.purgeOriginalImage(caseId, imageId);
      setImages((prev) =>
        prev.map((img) => (img.id === imageId ? { ...img, is_original_deleted: true } : img))
      );
      setStatusMessage("Raw image file purged from server. Fingerprint retained.");
    } catch (err: any) {
      alert(err.message || "Failed to purge image");
    }
  };

  const handleStartDiscovery = async () => {
    setIsDiscovering(true);
    try {
      await api.triggerDiscovery(caseId);
      setStatusMessage("Multi-platform discovery initiated across Meta, X, Reddit, YouTube, Bluesky & Web.");
      setTimeout(() => {
        router.push(`/cases/${caseId}/matches`);
      }, 1200);
    } catch (err: any) {
      alert(err.message || "Discovery failed to start");
      setIsDiscovering(false);
    }
  };

  const handleScanManualUrl = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!manualUrl.trim()) return;
    setIsScanningUrl(true);
    try {
      const match = await api.submitManualUrl(caseId, manualUrl.trim());
      if (match) {
        setStatusMessage(`Scanned URL! Match detected with similarity ${match.similarity_score}%.`);
      } else {
        setStatusMessage("Scanned URL: Content was analyzed, but no match exceeded threshold.");
      }
      setManualUrl("");
    } catch (err: any) {
      alert(err.message || "Failed to scan manual URL");
    } finally {
      setIsScanningUrl(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-[calc(100vh-64px)] flex items-center justify-center p-6 bg-canvas">
        <div className="flex items-center gap-2 text-sm text-muted">
          <RefreshCw className="w-4 h-4 animate-spin text-brand-pink" />
          <span>Loading case records...</span>
        </div>
      </div>
    );
  }

  if (!caseData) {
    return (
      <div className="min-h-[calc(100vh-64px)] p-12 text-center bg-canvas">
        <h2 className="text-xl font-medium text-ink mb-2">Case Not Found</h2>
        <p className="text-sm text-muted mb-6">This case may have been permanently purged.</p>
        <Link href="/dashboard">
          <Button>Return to Dashboard</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-[calc(100vh-64px)] py-10 px-6 md:px-12 bg-canvas">
      <div className="max-w-container mx-auto">
        {/* Case Navigation Tabs */}
        <div className="flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b border-hairline">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="font-mono text-xs font-semibold text-ink px-2 py-0.5 rounded-sm bg-surface-strong">
                {caseData.case_number}
              </span>
              <span className="text-xs px-2.5 py-0.5 rounded-pill bg-brand-teal/10 text-brand-teal font-medium">
                {caseData.status}
              </span>
              {caseData.is_anonymous && (
                <span className="text-xs px-2.5 py-0.5 rounded-pill bg-surface-card border border-hairline text-muted">
                  Anonymous Vault
                </span>
              )}
            </div>
            <h1 className="text-2xl sm:text-3xl font-medium text-ink tracking-tight">{caseData.title}</h1>
          </div>

          <div className="flex items-center gap-2">
            <Link
              href={`/cases/${caseId}/matches`}
              className="px-3.5 py-2 text-xs font-medium rounded-md bg-surface-card border border-hairline text-ink hover:bg-surface-strong transition-colors flex items-center gap-1.5"
            >
              <Search className="w-3.5 h-3.5 text-brand-pink" />
              <span>Review Matches</span>
            </Link>
            <Link
              href={`/cases/${caseId}/evidence`}
              className="px-3.5 py-2 text-xs font-medium rounded-md bg-surface-card border border-hairline text-ink hover:bg-surface-strong transition-colors flex items-center gap-1.5"
            >
              <FileCheck2 className="w-3.5 h-3.5 text-brand-teal" />
              <span>Evidence Vault</span>
            </Link>
            <Link
              href={`/cases/${caseId}/reports`}
              className="px-3.5 py-2 text-xs font-medium rounded-md bg-surface-card border border-hairline text-ink hover:bg-surface-strong transition-colors flex items-center gap-1.5"
            >
              <CheckCircle2 className="w-3.5 h-3.5 text-success" />
              <span>Takedown Reports</span>
            </Link>
          </div>
        </div>

        {/* Status Alert Banner */}
        {statusMessage && (
          <div className="mb-8 p-4 rounded-xl bg-surface-card border border-brand-pink/30 flex items-center gap-3 text-xs text-ink">
            <CheckCircle2 className="w-4 h-4 text-brand-pink flex-shrink-0" />
            <span className="font-medium">{statusMessage}</span>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column (8 cols): Upload Zone & Fingerprints */}
          <div className="lg:col-span-8 space-y-8">
            {/* Upload Zone Card */}
            <div className="bg-canvas border border-hairline rounded-xl p-8 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-lg font-medium text-ink">Fingerprint Source Media</h2>
                  <p className="text-xs text-muted">
                    Upload reference images or keyframe clips. Hashes are calculated in memory.
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-muted">Zero-Storage Mode:</span>
                  <span
                    className={`text-xs px-2 py-0.5 rounded-pill font-semibold ${
                      !retainEncrypted ? "bg-success/15 text-green-800" : "bg-warning/15 text-amber-800"
                    }`}
                  >
                    {!retainEncrypted ? "Purge Enabled" : "AES-256 Retained"}
                  </span>
                </div>
              </div>

              {/* Upload Dropzone */}
              <label className="border-2 border-dashed border-hairline hover:border-ink rounded-xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition-colors bg-surface-soft/40 hover:bg-surface-soft">
                <input
                  type="file"
                  accept="image/png,image/jpeg,image/webp,video/mp4"
                  onChange={handleFileUpload}
                  disabled={isUploading}
                  className="hidden"
                />
                <div className="w-12 h-12 rounded-full bg-surface-card flex items-center justify-center mb-3 text-brand-pink shadow-sm">
                  {isUploading ? (
                    <RefreshCw className="w-6 h-6 animate-spin" />
                  ) : (
                    <UploadCloud className="w-6 h-6" />
                  )}
                </div>
                <h3 className="text-sm font-semibold text-ink mb-1">
                  {isUploading ? "Computing Perceptual Hashes..." : "Click or Drag Media to Fingerprint"}
                </h3>
                <p className="text-xs text-muted max-w-sm mb-3">
                  Supports PNG, JPG, WebP, and MP4 keyframes. Original files are purged automatically after hashing.
                </p>
                <div className="inline-flex items-center gap-2 text-[11px] text-muted-soft bg-canvas px-3 py-1 rounded-pill border border-hairline">
                  <Lock className="w-3 h-3 text-brand-teal" />
                  <span>256-bit PDQ + pHash + dHash + SHA-256</span>
                </div>
              </label>

              {/* Retention Toggle */}
              <div className="mt-4 flex items-center justify-between text-xs text-muted pt-3 border-t border-hairline">
                <label className="flex items-center gap-2 cursor-pointer select-none">
                  <input
                    type="checkbox"
                    checked={retainEncrypted}
                    onChange={(e) => setRetainEncrypted(e.target.checked)}
                    className="w-4 h-4 accent-ink rounded cursor-pointer"
                  />
                  <span>Retain AES-256 encrypted original on server (optional for court exhibits)</span>
                </label>
              </div>
            </div>

            {/* Fingerprints Table */}
            <div className="bg-canvas border border-hairline rounded-xl overflow-hidden shadow-sm">
              <div className="p-6 border-b border-hairline flex items-center justify-between">
                <div>
                  <h3 className="text-base font-semibold text-ink">Active Perceptual Fingerprints</h3>
                  <p className="text-xs text-muted">
                    Mathematical representations used to match public re-uploads and crops.
                  </p>
                </div>
                <BadgePill>{images.length} Fingerprints</BadgePill>
              </div>

              {images.length === 0 ? (
                <div className="p-8 text-center text-xs text-muted">
                  No images fingerprinted yet. Upload your source file above to begin matching.
                </div>
              ) : (
                <div className="divide-y divide-hairline">
                  {images.map((img) => (
                    <div key={img.id} className="p-6 flex flex-col gap-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Fingerprint className="w-4 h-4 text-brand-pink" />
                          <span className="text-sm font-medium text-ink">{img.original_filename}</span>
                          <span className="text-xs text-muted">
                            ({(img.file_size_bytes / 1024).toFixed(1)} KB)
                          </span>
                        </div>
                        <div className="flex items-center gap-2">
                          {img.is_original_deleted ? (
                            <span className="text-[11px] font-semibold text-green-800 bg-success/15 px-2.5 py-0.5 rounded-pill border border-success/30">
                              ✓ Raw File Purged
                            </span>
                          ) : (
                            <button
                              onClick={() => handlePurge(img.id)}
                              className="text-[11px] text-error hover:underline flex items-center gap-1"
                            >
                              <Trash2 className="w-3 h-3" />
                              <span>Purge Original Now</span>
                            </button>
                          )}
                        </div>
                      </div>

                      {/* Hash Vector Details */}
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs bg-surface-card p-3 rounded-md border border-hairline font-mono">
                        <div>
                          <span className="text-muted block text-[10px]">PDQ HASH (256-bit Vector):</span>
                          <span className="text-ink truncate block text-[11px]">
                            {img.pdq_hash || "N/A"}
                          </span>
                        </div>
                        <div>
                          <span className="text-muted block text-[10px]">SHA-256 BITWISE EXACT:</span>
                          <span className="text-ink truncate block text-[11px]">{img.sha256}</span>
                        </div>
                        <div>
                          <span className="text-muted block text-[10px]">PERCEPTUAL pHASH:</span>
                          <span className="text-ink truncate block text-[11px]">
                            {img.phash || "N/A"}
                          </span>
                        </div>
                        <div>
                          <span className="text-muted block text-[10px]">DIFFERENCE dHASH:</span>
                          <span className="text-ink truncate block text-[11px]">
                            {img.dhash || "N/A"}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Right Column (4 cols): Discovery Controls & Manual URL Scan */}
          <div className="lg:col-span-4 space-y-6">
            {/* Primary Action Card: Run Discovery */}
            <div className="bg-brand-teal text-white rounded-xl p-6 shadow-md">
              <div className="flex items-center gap-2 text-brand-pink text-xs font-semibold uppercase tracking-wider mb-2">
                <Sparkles className="w-4 h-4" />
                <span>Automated Discovery</span>
              </div>
              <h3 className="text-xl font-medium mb-2">Scan Public Platforms</h3>
              <p className="text-white/80 text-xs leading-relaxed mb-6">
                Query Meta Graph API, X API, Reddit, YouTube Shorts, Bluesky, and Open Web indexes for matching
                perceptual fingerprints.
              </p>
              <button
                onClick={handleStartDiscovery}
                disabled={isDiscovering}
                className="w-full h-[44px] bg-brand-pink text-white font-semibold text-sm rounded-md hover:bg-brand-pink/90 transition-colors flex items-center justify-center gap-2 min-h-[44px]"
              >
                {isDiscovering ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Searching Platforms...</span>
                  </>
                ) : (
                  <>
                    <Search className="w-4 h-4" />
                    <span>Run Multi-Platform Discovery</span>
                  </>
                )}
              </button>
            </div>

            {/* Manual URL Inspection Form */}
            <div className="bg-canvas border border-hairline rounded-xl p-6 shadow-sm">
              <h3 className="text-sm font-semibold text-ink mb-1 flex items-center gap-1.5">
                <LinkIcon className="w-4 h-4 text-brand-teal" />
                <span>Scan Suspected URL Directly</span>
              </h3>
              <p className="text-xs text-muted mb-4">
                Have a specific link? We'll download the media transiently, compute its hash, and compare to this case.
              </p>
              <form onSubmit={handleScanManualUrl} className="space-y-3">
                <input
                  type="url"
                  required
                  value={manualUrl}
                  onChange={(e) => setManualUrl(e.target.value)}
                  placeholder="https://reddit.com/r/.../post"
                  className="w-full h-[42px] px-3.5 rounded-md bg-canvas border border-hairline text-ink text-xs focus:outline-none focus:border-ink transition-colors font-mono"
                />
                <Button
                  type="submit"
                  size="sm"
                  variant="secondary"
                  className="w-full"
                  isLoading={isScanningUrl}
                  leftIcon={<Search className="w-3.5 h-3.5" />}
                >
                  Verify URL Against Fingerprints
                </Button>
              </form>
            </div>

            {/* Case Overview Information */}
            <div className="bg-surface-card border border-hairline rounded-xl p-6 text-xs text-body space-y-3">
              <h4 className="font-semibold text-ink text-xs uppercase tracking-wider">Case Metadata</h4>
              <div className="flex justify-between py-1 border-b border-hairline">
                <span className="text-muted">Incident Date:</span>
                <span className="font-medium text-ink">{caseData.incident_date || "Undisclosed"}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-hairline">
                <span className="text-muted">Suspected Platforms:</span>
                <span className="font-medium text-ink">
                  {caseData.suspected_platforms?.join(", ") || "All permitted"}
                </span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-muted">Created:</span>
                <span className="font-medium text-ink">
                  {new Date(caseData.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
