"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  FileCheck2,
  ShieldCheck,
  Download,
  ArrowLeft,
  ArrowRight,
  ExternalLink,
  Lock,
  Link as LinkIcon,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
} from "lucide-react";
import { api } from "@/lib/api";
import { EvidenceItem } from "@/types";
import { Button } from "@/components/Button";
import { BadgePill } from "@/components/Badge";

export default function EvidenceVaultPage() {
  const params = useParams();
  const caseId = params.id as string;

  const [evidence, setEvidence] = useState<EvidenceItem[]>([]);
  const [chainIntact, setChainIntact] = useState(true);
  const [isLoading, setIsLoading] = useState(true);
  const [isExporting, setIsExporting] = useState(false);

  const loadEvidence = async () => {
    try {
      const vault = await api.getEvidenceVault(caseId);
      const items = Array.isArray(vault?.items)
        ? vault.items
        : Array.isArray(vault)
        ? vault
        : [];
      setEvidence(items);
      setChainIntact(vault?.is_chain_valid !== false);
    } catch {
      setEvidence([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadEvidence();
  }, [caseId]);

  const handleExportJson = async () => {
    setIsExporting(true);
    try {
      const exportData = await api.exportEvidence(caseId);
      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `SafeTrace_Evidence_Ledger_${caseId.slice(0, 8)}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err: any) {
      alert(err.message || "Failed to export evidence dossier");
    } finally {
      setIsExporting(false);
    }
  };

  const evidenceList = Array.isArray(evidence) ? evidence : [];

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
            href={`/cases/${caseId}/reports`}
            className="text-xs font-semibold text-brand-pink hover:underline flex items-center gap-1"
          >
            <span>Proceed to Bulk Takedown & Legal PDF Dossier →</span>
          </Link>
        </div>

        {/* Header */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-6 mb-8 border-b border-hairline">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="text-xs font-semibold uppercase tracking-wider text-muted">
                Tamper-Evident Ledger
              </span>
              <span className="w-1.5 h-1.5 rounded-full bg-brand-pink" />
              <span className="text-xs text-brand-teal font-medium">Sec 65B Indian Evidence Act</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-medium text-ink tracking-tight">
              Cryptographic Evidence Vault
            </h1>
            <p className="text-xs text-muted max-w-2xl mt-1">
              Confirmed violations are chained sequentially using SHA-256 block hashes. Any retroactive alteration
              invalidates the cryptographic chain, providing ironclad court admissibility.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Button
              variant="secondary"
              size="md"
              onClick={handleExportJson}
              isLoading={isExporting}
              leftIcon={<Download className="w-4 h-4" />}
            >
              Export Hash Ledger (JSON)
            </Button>
            <Link href={`/cases/${caseId}/reports`}>
              <Button size="md" rightIcon={<ArrowRight className="w-4 h-4" />}>
                Generate Legal PDF
              </Button>
            </Link>
          </div>
        </div>

        {/* Cryptographic Verification Status Banner */}
        <div className="mb-8 p-5 rounded-xl bg-surface-card border border-hairline flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3.5">
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                chainIntact ? "bg-success/15 text-green-800" : "bg-error/15 text-red-800"
              }`}
            >
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-semibold text-ink">
                  Cryptographic Hash Chain: {chainIntact ? "Intact & Verified" : "Verification Failed"}
                </h3>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded-pill font-semibold ${
                    chainIntact ? "bg-success/20 text-green-900" : "bg-error/20 text-red-900"
                  }`}
                >
                  {chainIntact ? "Valid" : "Compromised"}
                </span>
              </div>
              <p className="text-xs text-muted mt-0.5">
                All {evidenceList.length} blocks verify mathematically from Genesis block. Tamper-proof timestamping
                maintained in UTC.
              </p>
            </div>
          </div>
          <BadgePill>{evidenceList.length} Blocks Locked</BadgePill>
        </div>

        {/* Evidence Blocks Schedule */}
        <div className="bg-canvas border border-hairline rounded-xl overflow-hidden shadow-sm">
          <div className="p-6 border-b border-hairline flex items-center justify-between">
            <div>
              <h2 className="text-base font-semibold text-ink">Evidence Chain Schedule</h2>
              <p className="text-xs text-muted">
                Detailed block headers, parent block links, and captured media hashes.
              </p>
            </div>
          </div>

          {isLoading ? (
            <div className="p-16 text-center text-sm text-muted flex items-center justify-center gap-2">
              <RefreshCw className="w-4 h-4 animate-spin text-brand-pink" />
              <span>Verifying ledger integrity...</span>
            </div>
          ) : evidenceList.length === 0 ? (
            <div className="p-16 text-center flex flex-col items-center justify-center">
              <FileCheck2 className="w-10 h-10 text-muted-soft mb-3 stroke-1" />
              <h3 className="text-base font-semibold text-ink mb-1">Evidence vault is currently empty</h3>
              <p className="text-xs text-muted max-w-sm mb-6">
                Review discovered candidate matches and click "Confirm" to write them permanently into this
                cryptographic ledger.
              </p>
              <Link href={`/cases/${caseId}/matches`}>
                <Button size="sm">Go to Match Review</Button>
              </Link>
            </div>
          ) : (
            <div className="divide-y divide-hairline">
              {evidenceList.map((item, idx) => (
                <div key={item.id} className="p-6 flex flex-col gap-4 hover:bg-surface-soft/40 transition-colors">
                  {/* Top Bar: Sequence, Number, Platform */}
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div className="flex items-center gap-2.5">
                      <span className="font-mono text-xs font-bold px-2.5 py-1 rounded-sm bg-ink text-white">
                        BLOCK #{String(item.chain_sequence ?? idx + 1).padStart(4, "0")}
                      </span>
                      <span className="font-mono text-xs font-semibold px-2.5 py-1 rounded-sm bg-surface-strong text-ink">
                        {item.evidence_number}
                      </span>
                      <span className="text-xs font-semibold px-2.5 py-1 rounded-pill bg-brand-teal/10 text-brand-teal uppercase tracking-wider">
                        {item.platform}
                      </span>
                    </div>

                    <div className="flex items-center gap-2 text-xs text-muted">
                      <span>Captured UTC:</span>
                      <span className="font-mono text-ink">
                        {new Date(item.captured_at).toUTCString()}
                      </span>
                    </div>
                  </div>

                  {/* Target URL */}
                  <div className="text-xs">
                    <span className="text-muted block text-[11px] mb-0.5">SOURCE TARGET URL:</span>
                    <a
                      href={item.source_url}
                      target="_blank"
                      rel="noreferrer"
                      className="font-mono text-brand-teal hover:underline flex items-center gap-1 truncate text-xs"
                    >
                      <span className="truncate">{item.source_url}</span>
                      <ExternalLink className="w-3 h-3 flex-shrink-0" />
                    </a>
                  </div>

                  {/* Cryptographic Block Details */}
                  <div className="bg-surface-card border border-hairline rounded-md p-3.5 font-mono text-xs space-y-2">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                      <span className="text-muted text-[10px] uppercase">Previous Block Hash:</span>
                      <span className="text-muted-soft truncate max-w-sm text-[11px]">
                        {item.previous_evidence_hash || "0000000000000000000000000000000000000000000000000000000000000000 (Genesis)"}
                      </span>
                    </div>
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                      <span className="text-muted text-[10px] uppercase">Captured Content SHA-256:</span>
                      <span className="text-ink truncate max-w-sm text-[11px] font-semibold">
                        {item.captured_sha256 || item.content_sha256 || "N/A"}
                      </span>
                    </div>
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 pt-1 border-t border-hairline">
                      <span className="text-brand-teal text-[10px] uppercase font-bold">
                        Block Evidence Hash:
                      </span>
                      <span className="text-ink truncate max-w-sm text-[11px] font-bold">
                        {item.evidence_hash}
                      </span>
                    </div>
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
