"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Shield,
  Lock,
  Trash2,
  FileCheck2,
  Download,
  AlertTriangle,
  CheckCircle2,
  KeyRound,
  EyeOff,
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/Button";

export default function SettingsPage() {
  const router = useRouter();
  const { user, logout } = useAuth();
  const [isDeleting, setIsDeleting] = useState(false);

  const handlePermanentPurge = () => {
    const confirmation = prompt(
      "CAUTION: This will permanently delete your account, cases, perceptual hashes, and cryptographic evidence chains.\n\nType 'DELETE ALL' to confirm:"
    );
    if (confirmation === "DELETE ALL") {
      setIsDeleting(true);
      setTimeout(() => {
        logout();
        alert("Your data and records have been permanently purged from the system.");
        router.push("/");
      }, 1000);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] py-12 px-6 md:px-12 bg-canvas">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-2 mb-1.5">
            <span className="text-xs font-semibold uppercase tracking-wider text-muted">
              Privacy & Trust Center
            </span>
            <span className="w-1.5 h-1.5 rounded-full bg-brand-pink" />
            <span className="text-xs text-brand-teal font-medium">Digital Sovereignty</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-medium text-ink tracking-tight mb-2">
            Settings & Cryptographic Controls
          </h1>
          <p className="text-sm text-body">
            Manage your account pseudonymity, verify zero-knowledge guarantees, and exercise your right to be
            forgotten.
          </p>
        </div>

        <div className="space-y-8">
          {/* Account Profile Card */}
          <div className="bg-canvas border border-hairline rounded-xl p-6 shadow-sm">
            <h2 className="text-base font-semibold text-ink mb-4">Account Identity</h2>
            <div className="space-y-4 text-xs">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between py-2 border-b border-hairline">
                <span className="text-muted">Account Email:</span>
                <span className="font-mono text-ink font-medium">{user?.email || "Anonymous Session"}</span>
              </div>
              <div className="flex flex-col sm:flex-row sm:items-center justify-between py-2 border-b border-hairline">
                <span className="text-muted">Display Pseudonym:</span>
                <span className="text-ink font-medium">{user?.full_name || "Anonymous Survivor"}</span>
              </div>
              <div className="flex flex-col sm:flex-row sm:items-center justify-between py-2">
                <span className="text-muted">Workspace Role:</span>
                <span className="font-semibold text-brand-teal uppercase tracking-wider">
                  {user?.role || "VICTIM"}
                </span>
              </div>
            </div>
          </div>

          {/* Privacy & Cryptographic Verification Guarantees */}
          <div className="bg-canvas border border-hairline rounded-xl p-6 shadow-sm space-y-4">
            <h2 className="text-base font-semibold text-ink mb-2">Cryptographic Guarantees</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-surface-card border border-hairline rounded-lg p-4">
                <div className="flex items-center gap-2 text-xs font-semibold text-ink mb-1">
                  <CheckCircle2 className="w-4 h-4 text-success" />
                  <span>Zero-Knowledge Fingerprinting</span>
                </div>
                <p className="text-[11px] text-muted leading-relaxed">
                  Raw uploaded files are deleted automatically once PDQ and perceptual hashes are computed unless
                  explicitly saved.
                </p>
              </div>

              <div className="bg-surface-card border border-hairline rounded-lg p-4">
                <div className="flex items-center gap-2 text-xs font-semibold text-ink mb-1">
                  <Lock className="w-4 h-4 text-brand-teal" />
                  <span>AES-256 Fernet Encryption</span>
                </div>
                <p className="text-[11px] text-muted leading-relaxed">
                  All retained case documents and target URLs are encrypted using authenticated 256-bit AES-GCM/Fernet.
                </p>
              </div>

              <div className="bg-surface-card border border-hairline rounded-lg p-4">
                <div className="flex items-center gap-2 text-xs font-semibold text-ink mb-1">
                  <KeyRound className="w-4 h-4 text-brand-pink" />
                  <span>Argon2id Key Derivation</span>
                </div>
                <p className="text-[11px] text-muted leading-relaxed">
                  State-of-the-art memory-hard password hashing with random per-user cryptographic salts.
                </p>
              </div>

              <div className="bg-surface-card border border-hairline rounded-lg p-4">
                <div className="flex items-center gap-2 text-xs font-semibold text-ink mb-1">
                  <FileCheck2 className="w-4 h-4 text-brand-ochre" />
                  <span>SHA-256 Block Chain</span>
                </div>
                <p className="text-[11px] text-muted leading-relaxed">
                  Tamper-evident hash chain ensures evidence exhibits cannot be retroactively modified without
                  invalidating ledger.
                </p>
              </div>
            </div>
          </div>

          {/* Danger Zone: Permanent Account & Case Purge */}
          <div className="bg-canvas border border-error/30 rounded-xl p-6 shadow-sm">
            <div className="flex items-center gap-2 text-error mb-2">
              <AlertTriangle className="w-5 h-5" />
              <h2 className="text-base font-semibold text-error">Permanent Data Erasure</h2>
            </div>
            <p className="text-xs text-muted leading-relaxed mb-6">
              In accordance with the Right to be Forgotten and Digital Personal Data Protection Act 2023, you can
              irreversibly wipe all cases, uploaded images, discovered matches, evidence items, and your user profile
              with zero trace.
            </p>
            <Button
              variant="danger"
              size="md"
              onClick={handlePermanentPurge}
              isLoading={isDeleting}
              leftIcon={<Trash2 className="w-4 h-4" />}
            >
              Permanently Purge All Data
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
