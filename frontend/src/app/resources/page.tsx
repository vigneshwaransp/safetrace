import React from "react";
import Link from "next/link";
import {
  PhoneCall,
  ExternalLink,
  Shield,
  FileCheck2,
  Clock,
  Scale,
  CheckCircle2,
  AlertTriangle,
  HeartHandshake,
  ArrowRight,
} from "lucide-react";
import { Button } from "@/components/Button";

export default function ResourcesPage() {
  const officialChannels = [
    {
      name: "National Cyber Crime Reporting Portal",
      contact: "Helpline 1930 / cybercrime.gov.in",
      url: "https://cybercrime.gov.in",
      badge: "Government of India",
      description:
        "Official Ministry of Home Affairs portal for reporting cybercrimes against women and children. Offers an 'Anonymous Reporting' category for Non-Consensual Intimate Imagery.",
      guidelines: [
        "Select 'Report Cyber Crime Related to Women / Child' on the homepage.",
        "Choose 'Report Anonymously' if you do not want your identity displayed on police FIR.",
        "Upload the SafeTrace PDF Evidence Dossier as your primary Annexure exhibit.",
        "Provide exact URLs, timestamps in UTC, and captured SHA-256 hashes.",
      ],
      turnaround: "Assigned to state cyber cell within 24-48 hours",
    },
    {
      name: "StopNCII.org (Adult Image Hashing)",
      contact: "Operated by SWGfL & Global Tech Coalition",
      url: "https://stopncii.org",
      badge: "Industry Hash Partner",
      description:
        "Creates perceptual hash hashes directly on your local device and shares the hashes with participating tech giants (Meta, TikTok, OnlyFans, Bumble, etc.) to prevent uploads.",
      guidelines: [
        "Open StopNCII.org directly from your browser.",
        "Upload source images locally (raw files NEVER leave your browser).",
        "A case PIN is generated for you to track and withdraw hashes at any time.",
      ],
      turnaround: "Hash distributed to platforms within hours",
    },
    {
      name: "Take It Down (For Minors Under 18)",
      contact: "National Center for Missing & Exploited Children (NCMEC)",
      url: "https://takeitdown.ncmec.org",
      badge: "Global Youth Protection",
      description:
        "Free service operated by NCMEC to remove sexually explicit photos or videos taken of you when you were under 18 from public internet platforms.",
      guidelines: [
        "Select the category matching your age when the image was taken.",
        "Generate numerical hash vectors locally in browser.",
        "Platform automatically blocks re-uploads across participating networks.",
      ],
      turnaround: "Immediate hash sharing with platforms",
    },
    {
      name: "National Commission for Women (NCW)",
      contact: "7827170170 / ncw.nic.in",
      url: "http://ncw.nic.in",
      badge: "Statutory Authority",
      description:
        "Statutory body protecting women's rights in India. Maintains a 24/7 dedicated Cyber Crime Cell to intervene directly with DGP / Police Commissioners for swift FIR registration.",
      guidelines: [
        "Access the NCW online complaint registration portal.",
        "Categorize complaint under 'Cyber Crime Against Women'.",
        "Attach the SafeTrace ReportLab Dossier with full hash ledger.",
      ],
      turnaround: "Immediate notice issued to concerned police cyber cell",
    },
  ];

  return (
    <div className="min-h-[calc(100vh-64px)] py-12 px-6 md:px-12 bg-canvas">
      <div className="max-w-container mx-auto">
        {/* Header */}
        <div className="max-w-2xl mb-12">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-pill bg-brand-pink/15 text-brand-pink text-xs font-semibold mb-4 border border-brand-pink/30">
            <HeartHandshake className="w-3.5 h-3.5" />
            <span>Crisis & Legal Guidance Sanctuary</span>
          </div>
          <h1 className="text-3xl sm:text-4xl lg:text-[48px] font-medium text-ink tracking-tight mb-4 leading-tight">
            Official Channels & Statutory Rights
          </h1>
          <p className="text-sm sm:text-base text-body leading-relaxed">
            SafeTrace assists you in gathering verifiable evidence. Below are the verified government helplines,
            industry prevention databases, and legal frameworks under Indian law to help you achieve swift takedowns.
          </p>
        </div>

        {/* 24/7 Emergency Helpline Cards (3-up) */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
          <div className="bg-surface-card border border-hairline rounded-xl p-6 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-semibold uppercase tracking-wider text-muted">
                  Cyber Financial & Extortion
                </span>
                <span className="w-2.5 h-2.5 rounded-full bg-error" />
              </div>
              <h3 className="text-2xl font-bold text-ink mb-1">1930</h3>
              <p className="text-xs text-muted leading-relaxed mb-4">
                National Cyber Crime Helpline (Ministry of Home Affairs). 24/7 toll-free emergency call center.
              </p>
            </div>
            <a
              href="tel:1930"
              className="w-full h-[40px] bg-ink text-white text-xs font-semibold rounded-md flex items-center justify-center gap-2 hover:bg-neutral-800 transition-colors min-h-[40px]"
            >
              <PhoneCall className="w-3.5 h-3.5" />
              <span>Call 1930 Immediately</span>
            </a>
          </div>

          <div className="bg-surface-card border border-hairline rounded-xl p-6 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-semibold uppercase tracking-wider text-muted">
                  Women Helpline (Universal)
                </span>
                <span className="w-2.5 h-2.5 rounded-full bg-brand-pink" />
              </div>
              <h3 className="text-2xl font-bold text-ink mb-1">181</h3>
              <p className="text-xs text-muted leading-relaxed mb-4">
                24/7 emergency response for women affected by cyber harassment, blackmail, and domestic distress.
              </p>
            </div>
            <a
              href="tel:181"
              className="w-full h-[40px] bg-surface-strong border border-hairline text-ink text-xs font-semibold rounded-md flex items-center justify-center gap-2 hover:bg-surface-card transition-colors min-h-[40px]"
            >
              <PhoneCall className="w-3.5 h-3.5" />
              <span>Call 181 Women Helpline</span>
            </a>
          </div>

          <div className="bg-surface-card border border-hairline rounded-xl p-6 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-semibold uppercase tracking-wider text-muted">
                  NCW WhatsApp Helpline
                </span>
                <span className="w-2.5 h-2.5 rounded-full bg-brand-teal" />
              </div>
              <h3 className="text-xl font-bold text-ink mb-1">+91 7827-170-170</h3>
              <p className="text-xs text-muted leading-relaxed mb-4">
                Direct WhatsApp and phone assistance by National Commission for Women Cyber Cell officers.
              </p>
            </div>
            <a
              href="https://wa.me/917827170170"
              target="_blank"
              rel="noreferrer"
              className="w-full h-[40px] bg-surface-strong border border-hairline text-ink text-xs font-semibold rounded-md flex items-center justify-center gap-2 hover:bg-surface-card transition-colors min-h-[40px]"
            >
              <ExternalLink className="w-3.5 h-3.5" />
              <span>Message NCW on WhatsApp</span>
            </a>
          </div>
        </div>

        {/* Official Channels Breakdown Grid */}
        <div className="mb-16">
          <h2 className="text-2xl font-medium text-ink mb-6">Official Reporting Portals</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {officialChannels.map((channel, idx) => (
              <div key={idx} className="bg-canvas border border-hairline rounded-xl p-8 flex flex-col justify-between shadow-sm">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-semibold px-2.5 py-0.5 rounded-pill bg-brand-teal text-white">
                      {channel.badge}
                    </span>
                    <span className="text-xs font-mono text-muted">{channel.contact}</span>
                  </div>
                  <h3 className="text-lg font-semibold text-ink mb-2">{channel.name}</h3>
                  <p className="text-xs text-muted leading-relaxed mb-6">{channel.description}</p>

                  <div className="bg-surface-soft/60 rounded-md p-4 border border-hairline mb-6">
                    <span className="text-xs font-semibold text-ink block mb-2">Step-by-Step Submission:</span>
                    <ul className="space-y-1.5 text-xs text-body">
                      {channel.guidelines.map((g, gIdx) => (
                        <li key={gIdx} className="flex items-start gap-2">
                          <span className="text-brand-pink font-bold mt-0.5">•</span>
                          <span>{g}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div className="pt-4 border-t border-hairline flex items-center justify-between">
                  <span className="text-[11px] text-muted">
                    Response: <span className="font-medium text-ink">{channel.turnaround}</span>
                  </span>
                  <a
                    href={channel.url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1.5 text-xs font-semibold text-brand-pink hover:underline"
                  >
                    <span>Open Official Portal</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Legal Framework Explainer (IT Act & BNS) */}
        <div className="bg-surface-card border border-hairline rounded-xl p-8">
          <div className="flex items-center gap-2 mb-3">
            <Scale className="w-5 h-5 text-brand-teal" />
            <h2 className="text-lg font-semibold text-ink">Your Legal Rights Under Indian Law</h2>
          </div>
          <p className="text-xs text-muted max-w-2xl mb-6">
            Non-consensual image abuse, deepfake morphing, and sextortion violate both criminal penal statutes and
            intermediary digital rules.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
            <div className="bg-canvas border border-hairline rounded-md p-4">
              <h4 className="font-bold text-ink mb-1">IT Rules 2021 · Rule 3(2)(b)</h4>
              <p className="text-muted leading-relaxed">
                Mandates that social media platforms (Meta, X, Reddit) must remove non-consensual sexually explicit or
                morphed imagery within <span className="font-semibold text-ink">24 hours</span> of receiving a grievance.
              </p>
            </div>

            <div className="bg-canvas border border-hairline rounded-md p-4">
              <h4 className="font-bold text-ink mb-1">IT Act 2000 · Section 66E</h4>
              <p className="text-muted leading-relaxed">
                Punishes capturing, transmitting, or publishing images of a person's private areas without consent with up
                to 3 years imprisonment or fine up to ₹2 Lakh.
              </p>
            </div>

            <div className="bg-canvas border border-hairline rounded-md p-4">
              <h4 className="font-bold text-ink mb-1">IT Act 2000 · Section 67A</h4>
              <p className="text-muted leading-relaxed">
                Penalizes publishing or transmitting sexually explicit material electronically with imprisonment up to 5
                years and ₹10 Lakh fine.
              </p>
            </div>

            <div className="bg-canvas border border-hairline rounded-md p-4">
              <h4 className="font-bold text-ink mb-1">BNS 2023 · Sections 354C & 354D</h4>
              <p className="text-muted leading-relaxed">
                Bharatiya Nyaya Sanhita criminalizes voyeurism and digital cyberstalking of women with non-bailable
                imprisonment on second conviction.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
