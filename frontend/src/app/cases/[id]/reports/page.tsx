"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  FileText,
  FileCheck2,
  Download,
  Copy,
  Check,
  ArrowLeft,
  ExternalLink,
  Shield,
  Clock,
  Sparkles,
  AlertCircle,
  RefreshCw,
  Send,
} from "lucide-react";
import { api } from "@/lib/api";
import { EvidenceItem, Report, ReportStatus } from "@/types";
import { StatusBadge, BadgePill } from "@/components/Badge";
import { Button } from "@/components/Button";

const TARGET_PLATFORMS = [
  "REDDIT",
  "META_INSTAGRAM",
  "X_TWITTER",
  "YOUTUBE",
  "BLUESKY",
  "CYBERCRIME_GOV_IN",
  "GENERAL_HOST",
];

export default function ReportsPage() {
  const params = useParams();
  const caseId = params.id as string;

  const [evidenceList, setEvidenceList] = useState<EvidenceItem[]>([]);
  const [selectedEvidenceIds, setSelectedEvidenceIds] = useState<string[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [targetPlatform, setTargetPlatform] = useState("REDDIT");
  const [aliasName, setAliasName] = useState("");
  const [customNotes, setCustomNotes] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [selectedReportView, setSelectedReportView] = useState<Report | null>(null);
  const [updatingReportId, setUpdatingReportId] = useState<string | null>(null);
  const [downloadingReportId, setDownloadingReportId] = useState<string | null>(null);

  const loadData = async () => {
    try {
      const [evData, repData] = await Promise.all([
        api.getEvidenceItems(caseId).catch(() => []),
        api.getReports(caseId).catch(() => []),
      ]);
      const safeEvList = Array.isArray(evData) ? evData : [];
      const safeRepList = Array.isArray(repData) ? repData : [];
      setEvidenceList(safeEvList);
      setReports(safeRepList);
      // Select all by default
      setSelectedEvidenceIds(safeEvList.map((e) => e.id));
    } catch {
      setEvidenceList([]);
      setReports([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [caseId]);

  const toggleSelectEvidence = (id: string) => {
    if (selectedEvidenceIds.includes(id)) {
      setSelectedEvidenceIds(selectedEvidenceIds.filter((item) => item !== id));
    } else {
      setSelectedEvidenceIds([...selectedEvidenceIds, id]);
    }
  };

  const handleGenerateReport = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedEvidenceIds.length === 0) {
      alert("Please select at least one confirmed evidence block.");
      return;
    }
    setIsGenerating(true);
    try {
      const newRep = await api.createReport(caseId, {
        platform: targetPlatform,
        selected_evidence_ids: selectedEvidenceIds,
        victim_name_alias: aliasName || undefined,
        custom_notes: customNotes || undefined,
        generate_pdf: true,
      });
      setReports((prev) => [newRep, ...prev]);
      setSelectedReportView(newRep);
      alert("Generated takedown notice & official ReportLab PDF!");
    } catch (err: any) {
      alert(err.message || "Failed to generate report");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleStatusUpdate = async (reportId: string, newStatus: ReportStatus) => {
    setUpdatingReportId(reportId);
    try {
      const ticketId =
        newStatus === "SUBMITTED"
          ? prompt("Optional: Enter platform ticket / acknowledgement ID:") || undefined
          : undefined;

      const updated = await api.updateReportStatus(reportId, newStatus, undefined, ticketId);
      setReports((prev) => prev.map((r) => (r.id === reportId ? updated : r)));
    } catch (err: any) {
      alert(err.message || "Failed to update report status");
    } finally {
      setUpdatingReportId(null);
    }
  };

  const handleCopyNotice = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleDownloadPdf = async (reportId: string, reportNumber?: string) => {
    setDownloadingReportId(reportId);
    try {
      await api.downloadReportPdf(reportId, `SafeTrace_${reportNumber || reportId.slice(0, 8)}.pdf`);
    } catch (err: any) {
      alert(err.message || "Failed to download PDF dossier");
    } finally {
      setDownloadingReportId(null);
    }
  };

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
          <Link
            href="/resources"
            className="text-xs font-semibold text-brand-teal hover:underline flex items-center gap-1"
          >
            <span>View Official Reporting Form Directory →</span>
          </Link>
        </div>

        {/* Header */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-6 mb-8 border-b border-hairline">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="text-xs font-semibold uppercase tracking-wider text-muted">
                Statutory Takedown & Dossier
              </span>
              <span className="w-1.5 h-1.5 rounded-full bg-brand-pink" />
              <span className="text-xs text-brand-teal font-medium">IT Rules 2021 Rule 3(2)(b)</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-medium text-ink tracking-tight">
              Bulk Takedown Reports & Legal Dossiers
            </h1>
            <p className="text-xs text-muted max-w-2xl mt-1">
              Assemble multiple verified evidence blocks into formal statutory notices and downloadable ReportLab PDF
              complaints formatted for cybercrime portals and intermediary grievance officers.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column (5 cols): Generate New Report Form */}
          <div className="lg:col-span-5 space-y-6">
            <div className="bg-canvas border border-hairline rounded-xl p-6 shadow-sm">
              <h2 className="text-base font-semibold text-ink mb-1">Assemble Statutory Complaint</h2>
              <p className="text-xs text-muted mb-4">
                Select target destination and evidence blocks to compile.
              </p>

              <form onSubmit={handleGenerateReport} className="space-y-4">
                {/* Target Platform */}
                <div>
                  <label className="block text-xs font-semibold text-ink uppercase tracking-wider mb-1.5">
                    Target Platform / Entity
                  </label>
                  <select
                    value={targetPlatform}
                    onChange={(e) => setTargetPlatform(e.target.value)}
                    className="w-full h-[42px] px-3 rounded-md bg-canvas border border-hairline text-ink text-xs focus:outline-none focus:border-ink font-medium"
                  >
                    {TARGET_PLATFORMS.map((p) => (
                      <option key={p} value={p}>
                        {p.replace(/_/g, " ")}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Victim Alias */}
                <div>
                  <label className="block text-xs font-semibold text-ink uppercase tracking-wider mb-1.5">
                    Complainant Name / Pseudonym
                  </label>
                  <input
                    type="text"
                    value={aliasName}
                    onChange={(e) => setAliasName(e.target.value)}
                    placeholder="e.g. Maya or Aggrieved Party"
                    className="w-full h-[42px] px-3.5 rounded-md bg-canvas border border-hairline text-ink text-xs focus:outline-none focus:border-ink"
                  />
                </div>

                {/* Custom Narrative */}
                <div>
                  <label className="block text-xs font-semibold text-ink uppercase tracking-wider mb-1.5">
                    Additional Statements (Optional)
                  </label>
                  <textarea
                    rows={2}
                    value={customNotes}
                    onChange={(e) => setCustomNotes(e.target.value)}
                    placeholder="e.g. Content was obtained without consent and is being circulated for extortion."
                    className="w-full p-3 rounded-md bg-canvas border border-hairline text-ink text-xs focus:outline-none focus:border-ink resize-none"
                  />
                </div>

                {/* Evidence Item Selection */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-xs font-semibold text-ink uppercase tracking-wider">
                      Include Evidence Blocks ({selectedEvidenceIds.length}/{evidenceList.length})
                    </label>
                    <button
                      type="button"
                      onClick={() =>
                        setSelectedEvidenceIds(
                          selectedEvidenceIds.length === evidenceList.length
                            ? []
                            : evidenceList.map((e) => e.id)
                        )
                      }
                      className="text-[11px] text-brand-pink font-semibold hover:underline"
                    >
                      {selectedEvidenceIds.length === evidenceList.length ? "Deselect All" : "Select All"}
                    </button>
                  </div>

                  {evidenceList.length === 0 ? (
                    <div className="p-4 rounded-md bg-surface-card border border-hairline text-center text-xs text-muted">
                      No confirmed evidence blocks yet. Confirm matches first.
                    </div>
                  ) : (
                    <div className="max-h-48 overflow-y-auto space-y-2 border border-hairline rounded-md p-2 bg-surface-soft/40">
                      {evidenceList.map((ev) => {
                        const isSelected = selectedEvidenceIds.includes(ev.id);
                        return (
                          <div
                            key={ev.id}
                            onClick={() => toggleSelectEvidence(ev.id)}
                            className={`p-2 rounded cursor-pointer border text-xs flex items-center justify-between transition-colors ${
                              isSelected
                                ? "bg-surface-card border-ink font-medium text-ink"
                                : "bg-canvas border-hairline text-muted hover:bg-surface-soft"
                            }`}
                          >
                            <div className="flex items-center gap-2 truncate">
                              <span className="font-mono text-[11px] font-semibold">
                                {ev.evidence_number}
                              </span>
                              <span className="text-[10px] uppercase px-1.5 py-0.2 rounded bg-surface-strong">
                                {ev.platform}
                              </span>
                              <span className="truncate text-muted text-[11px] max-w-[140px]">
                                {ev.source_url}
                              </span>
                            </div>
                            <input
                              type="checkbox"
                              checked={isSelected}
                              readOnly
                              className="accent-ink w-3.5 h-3.5 pointer-events-none"
                            />
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>

                <Button
                  type="submit"
                  size="md"
                  className="w-full"
                  isLoading={isGenerating}
                  disabled={evidenceList.length === 0}
                  leftIcon={<Sparkles className="w-4 h-4" />}
                >
                  Generate Statutory Notice & PDF
                </Button>
              </form>
            </div>
          </div>

          {/* Right Column (7 cols): Existing Generated Reports & Status Progression */}
          <div className="lg:col-span-7 space-y-6">
            <div className="bg-canvas border border-hairline rounded-xl overflow-hidden shadow-sm">
              <div className="p-6 border-b border-hairline flex items-center justify-between">
                <div>
                  <h2 className="text-base font-semibold text-ink">Active Takedown Complaints</h2>
                  <p className="text-xs text-muted">
                    Track platform removal status and download official PDF complaint packages.
                  </p>
                </div>
                <BadgePill>{reports.length} Reports</BadgePill>
              </div>

              {reports.length === 0 ? (
                <div className="p-12 text-center text-xs text-muted flex flex-col items-center justify-center">
                  <FileText className="w-10 h-10 text-muted-soft mb-2 stroke-1" />
                  <span>No reports compiled yet. Use the generator on the left.</span>
                </div>
              ) : (
                <div className="divide-y divide-hairline">
                  {reports.map((rep) => (
                    <div key={rep.id} className="p-6 space-y-4">
                      {/* Report Header */}
                      <div className="flex flex-wrap items-center justify-between gap-3">
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-xs px-2.5 py-1 rounded-pill bg-brand-teal text-white uppercase tracking-wider">
                            {rep.platform || rep.recipient_platform || "PLATFORM"}
                          </span>
                          <StatusBadge status={rep.status as any} />
                          {rep.platform_ticket_id && (
                            <span className="font-mono text-xs text-muted bg-surface-card px-2 py-0.5 rounded border border-hairline">
                              Ticket: {rep.platform_ticket_id}
                            </span>
                          )}
                        </div>

                        <div className="flex items-center gap-2">
                          {(rep.has_pdf || rep.pdf_available || rep.pdf_storage_path) && (
                            <button
                              type="button"
                              onClick={() => handleDownloadPdf(rep.id, rep.report_number)}
                              disabled={downloadingReportId === rep.id}
                              className="px-3 py-1.5 bg-ink text-white text-xs font-semibold rounded-md hover:bg-neutral-800 transition-colors flex items-center gap-1.5 shadow-sm disabled:opacity-60"
                            >
                              <Download className={`w-3.5 h-3.5 ${downloadingReportId === rep.id ? "animate-spin text-brand-pink" : ""}`} />
                              <span>{downloadingReportId === rep.id ? "Downloading..." : "Download PDF Dossier"}</span>
                            </button>
                          )}
                        </div>
                      </div>

                      {/* Statutory Basis Badges */}
                      {rep.statutory_basis && rep.statutory_basis.length > 0 && (
                        <div className="flex flex-wrap items-center gap-1.5 text-[11px] text-muted">
                          <span className="font-medium text-ink">Statutory Basis:</span>
                          {rep.statutory_basis.map((s, idx) => (
                            <span key={idx} className="bg-surface-card px-2 py-0.5 rounded border border-hairline font-mono text-[10px]">
                              {s}
                            </span>
                          ))}
                        </div>
                      )}

                      {/* Actions: View Text & Copy */}
                      <div className="flex items-center gap-3 pt-1">
                        <button
                          onClick={() => setSelectedReportView(rep)}
                          className="text-xs font-semibold text-brand-teal hover:underline flex items-center gap-1"
                        >
                          <FileText className="w-3.5 h-3.5" />
                          <span>View Notice Text</span>
                        </button>

                        <button
                          onClick={() => handleCopyNotice(rep.report_text || rep.report_content || "", rep.id)}
                          className="text-xs font-semibold text-body hover:text-ink flex items-center gap-1"
                        >
                          {copiedId === rep.id ? (
                            <>
                              <Check className="w-3.5 h-3.5 text-success" />
                              <span className="text-success">Copied to Clipboard!</span>
                            </>
                          ) : (
                            <>
                              <Copy className="w-3.5 h-3.5 text-muted" />
                              <span>Copy Takedown Notice Text</span>
                            </>
                          )}
                        </button>
                      </div>

                      {/* Status Progression Controls */}
                      <div className="bg-surface-card rounded-md p-3 border border-hairline flex flex-wrap items-center justify-between gap-3 text-xs">
                        <span className="text-muted text-[11px]">Update Progression:</span>
                        <div className="flex flex-wrap items-center gap-2">
                          <button
                            onClick={() => handleStatusUpdate(rep.id, "SUBMITTED")}
                            disabled={updatingReportId === rep.id}
                            className="px-2.5 py-1 rounded bg-canvas border border-hairline hover:bg-surface-strong text-ink text-[11px] font-medium"
                          >
                            Mark Submitted
                          </button>
                          <button
                            onClick={() => handleStatusUpdate(rep.id, "ACKNOWLEDGED")}
                            disabled={updatingReportId === rep.id}
                            className="px-2.5 py-1 rounded bg-canvas border border-hairline hover:bg-surface-strong text-ink text-[11px] font-medium"
                          >
                            Mark Acknowledged
                          </button>
                          <button
                            onClick={() => handleStatusUpdate(rep.id, "REMOVED")}
                            disabled={updatingReportId === rep.id}
                            className="px-2.5 py-1 rounded bg-success/20 text-green-900 border border-success/30 hover:bg-success/30 text-[11px] font-semibold"
                          >
                            ✓ Mark Removed / Offline
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Modal / Preview of Notice Text */}
            {selectedReportView && (
              <div className="bg-surface-card border border-hairline rounded-xl p-6 shadow-sm">
                <div className="flex items-center justify-between mb-3 pb-3 border-b border-hairline">
                  <h3 className="text-sm font-semibold text-ink">
                    Takedown Grievance Text ({selectedReportView.recipient_platform || selectedReportView.platform})
                  </h3>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => handleDownloadPdf(selectedReportView.id, selectedReportView.report_number)}
                      disabled={downloadingReportId === selectedReportView.id}
                      className="px-2.5 py-1 bg-ink text-white text-xs font-medium rounded hover:bg-neutral-800 transition-colors flex items-center gap-1 shadow-sm"
                    >
                      <Download className="w-3 h-3" />
                      <span>Download PDF</span>
                    </button>
                    <button
                      onClick={() => setSelectedReportView(null)}
                      className="text-xs text-muted hover:text-ink font-semibold ml-2"
                    >
                      ✕
                    </button>
                  </div>
                </div>
                <pre className="text-xs font-mono text-body whitespace-pre-wrap max-h-72 overflow-y-auto bg-canvas p-4 rounded-md border border-hairline leading-relaxed">
                  {selectedReportView.report_text || selectedReportView.report_content}
                </pre>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
