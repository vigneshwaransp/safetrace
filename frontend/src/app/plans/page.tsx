import React from "react";
import Link from "next/link";
import { Check, ShieldCheck, Heart, Sparkles, ArrowRight } from "lucide-react";
import { PricingTierCard } from "@/components/Card";
import { Button } from "@/components/Button";

export default function PlansPage() {
  return (
    <div className="min-h-[calc(100vh-64px)] py-16 px-6 md:px-12 bg-canvas">
      <div className="max-w-container mx-auto">
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-pill bg-brand-pink/15 text-brand-pink text-xs font-semibold mb-4 border border-brand-pink/30">
            <Heart className="w-3.5 h-3.5" />
            <span>Survivor First Mission</span>
          </div>
          <h1 className="text-3xl sm:text-4xl lg:text-[56px] font-medium text-ink tracking-tight mb-4 leading-tight">
            Safety and dignity should never have a price tag.
          </h1>
          <p className="text-base text-body leading-relaxed">
            SafeTrace is completely free for all individual survivors. Institutional, legal clinic, and enterprise tiers
            subsidize our infrastructure and continuous Celery Beat monitoring.
          </p>
        </div>

        {/* Pricing Cards (3-up) */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto mb-20">
          <PricingTierCard
            title="Survivor Sanctuary"
            price="₹0"
            billingPeriod="forever free"
            description="Complete protection for individual women and victims of digital harassment."
            features={[
              "Unlimited zero-knowledge image fingerprinting",
              "Multi-platform discovery (Meta, X, Reddit, YT, Web)",
              "Human-in-the-loop review interface",
              "Cryptographic hash chain evidence ledger",
              "ReportLab PDF statutory complaint dossiers",
              "24/7 Celery Beat URL liveness scans",
              "Zero-storage raw image deletion guarantee",
            ]}
            ctaText="Create Free Protected Case"
            ctaHref="/auth/register"
          />

          <PricingTierCard
            title="Advocate & NGO"
            price="₹2,499"
            billingPeriod="/month (or grant subsidized)"
            description="Dedicated workspace for legal aid lawyers, cyber counselors, and survivor advocacy groups."
            features={[
              "Everything in Survivor, plus:",
              "Multi-client case management dashboard",
              "Consolidated statutory filing bundles",
              "Priority discovery background workers",
              "Client pseudonymity management",
              "Audit log export for court affidavits",
              "Multi-seat collaboration for counselors",
            ]}
            isFeatured={true}
            ctaText="Start NGO Workspace"
            ctaHref="/auth/register?role=NGO"
          />

          <PricingTierCard
            title="Institutional & Platforms"
            price="Custom"
            billingPeriod="annual partnership"
            description="For universities, platforms, and law enforcement agencies requiring private infrastructure."
            features={[
              "Private VPC / On-Premise Docker cluster",
              "Direct Law Enforcement portal bridges",
              "Air-gapped database deployment",
              "Custom PlatformConnector integrations",
              "24/7 Dedicated Trust & Safety Architect SLA",
              "Bespoke perceptual model tuning",
            ]}
            ctaText="Contact Safety Architects"
            ctaHref="/resources"
          />
        </div>

        {/* Feature Comparison Table */}
        <div className="max-w-4xl mx-auto bg-surface-card border border-hairline rounded-xl overflow-hidden mb-20">
          <div className="p-6 border-b border-hairline">
            <h2 className="text-lg font-medium text-ink">Feature Comparison Matrix</h2>
            <p className="text-xs text-muted">
              Every critical safety feature is available on the free survivor tier.
            </p>
          </div>
          <div className="overflow-x-auto text-xs">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-hairline bg-surface-soft/60">
                  <th className="p-4 font-semibold text-ink">Capability</th>
                  <th className="p-4 font-semibold text-ink text-center">Survivor (Free)</th>
                  <th className="p-4 font-semibold text-ink text-center">Advocate / NGO</th>
                  <th className="p-4 font-semibold text-ink text-center">Institutional</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-hairline">
                <tr>
                  <td className="p-4 font-medium text-ink">Zero-Knowledge Perceptual Hashing (PDQ/pHash)</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                </tr>
                <tr>
                  <td className="p-4 font-medium text-ink">Multi-Platform Discovery Sweep</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                  <td className="p-4 text-center text-success font-bold">✓ (Priority)</td>
                  <td className="p-4 text-center text-success font-bold">✓ (Realtime)</td>
                </tr>
                <tr>
                  <td className="p-4 font-medium text-ink">Tamper-Evident SHA-256 Hash Chain</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                </tr>
                <tr>
                  <td className="p-4 font-medium text-ink">Statutory ReportLab PDF Dossiers</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                </tr>
                <tr>
                  <td className="p-4 font-medium text-ink">24/7 Celery Beat Liveness Monitoring</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                </tr>
                <tr>
                  <td className="p-4 font-medium text-ink">Multi-Client Case Management</td>
                  <td className="p-4 text-center text-muted font-bold">—</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                </tr>
                <tr>
                  <td className="p-4 font-medium text-ink">On-Premise / Air-gapped Deployment</td>
                  <td className="p-4 text-center text-muted font-bold">—</td>
                  <td className="p-4 text-center text-muted font-bold">—</td>
                  <td className="p-4 text-center text-success font-bold">✓</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
