import React from "react";
import Link from "next/link";
import {
  ShieldCheck,
  Search,
  Lock,
  FileCheck2,
  RefreshCw,
  EyeOff,
  Scale,
  Sparkles,
  ArrowRight,
  Fingerprint,
  Link as LinkIcon,
  Shield,
  Clock,
  CheckCircle2,
} from "lucide-react";
import { HeroClayScene, EmptyStateClay, SecurityShieldClay } from "@/components/ClayIllustrations";
import { FeatureCard, ProductMockupCard, TestimonialCard, PricingTierCard } from "@/components/Card";
import { Button } from "@/components/Button";

export default function LandingPage() {
  return (
    <div className="flex flex-col">
      {/* 1. HERO BAND (7/5 Split: Text Left, Clay Illustration Right, 96px vertical rhythm) */}
      <section className="py-20 md:py-24 px-6 md:px-12 bg-canvas">
        <div className="max-w-container mx-auto grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Column (7 cols) */}
          <div className="lg:col-span-7 flex flex-col items-start">
            {/* Pill Badge */}
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-pill bg-brand-pink/15 text-brand-pink text-xs font-semibold mb-6 border border-brand-pink/30">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Digital Safety & Survivor Sanctuary · K-Hacks 4.0</span>
            </div>

            {/* Display Heading */}
            <h1 className="text-4xl sm:text-5xl lg:text-[72px] font-medium leading-[1.05] tracking-[-0.035em] text-ink mb-6">
              Reclaim control of your images with{" "}
              <span className="text-brand-pink underline decoration-brand-peach/60 decoration-wavy decoration-2">
                zero exposure.
              </span>
            </h1>

            {/* Subheading */}
            <p className="text-base sm:text-lg text-body leading-relaxed max-w-xl mb-8">
              SafeTrace empowers survivors of non-consensual image abuse to compute cryptographic perceptual
              fingerprints, discover unauthorized copies across public platforms, safeguard tamper-evident evidence, and
              expedite platform takedowns.
            </p>

            {/* Action Buttons */}
            <div className="flex flex-wrap items-center gap-4 w-full sm:w-auto">
              <Link href="/auth/register" className="w-full sm:w-auto">
                <Button size="lg" className="w-full sm:w-auto" rightIcon={<ArrowRight className="w-4 h-4" />}>
                  Create Anonymous Case
                </Button>
              </Link>
              <Link href="/#solution" className="w-full sm:w-auto">
                <Button variant="secondary" size="lg" className="w-full sm:w-auto">
                  How Fingerprinting Works
                </Button>
              </Link>
            </div>

            {/* Trust Assurances */}
            <div className="mt-10 flex flex-wrap items-center gap-6 text-xs text-muted">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-brand-teal" />
                <span>Zero-knowledge hashing (media purged)</span>
              </div>
              <div className="flex items-center gap-2">
                <Lock className="w-4 h-4 text-brand-teal" />
                <span>AES-256 encrypted vault</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-brand-teal" />
                <span>IT Act 66E / 67A Statutory format</span>
              </div>
            </div>
          </div>

          {/* Right Column (5 cols): Clay Illustration Card */}
          <div className="lg:col-span-5 flex items-center justify-center">
            <div className="w-full max-w-lg bg-surface-soft border border-hairline rounded-xl p-8 flex flex-col items-center shadow-sm relative overflow-hidden">
              <div className="absolute top-4 left-4 bg-canvas/80 backdrop-blur-sm border border-hairline px-3 py-1 rounded-pill text-[11px] font-medium text-ink flex items-center gap-1.5">
                <Fingerprint className="w-3.5 h-3.5 text-brand-pink" />
                <span>Cryptographic Perceptual Vault</span>
              </div>
              <HeroClayScene className="mt-6" />
              <div className="mt-4 text-center">
                <span className="text-xs font-semibold text-ink">Original Media Never Saved</span>
                <p className="text-[11px] text-muted max-w-xs mt-0.5">
                  Transient hashes detect copies even if cropped, compressed, or filtered.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. THE PROBLEM (5 Pain Points Feature Cards cycling colors: pink -> teal -> lavender -> peach -> ochre) */}
      <section id="problem" className="py-24 px-6 md:px-12 bg-surface-soft border-t border-hairline">
        <div className="max-w-container mx-auto">
          <div className="max-w-2xl mb-16">
            <span className="text-xs font-semibold uppercase tracking-wider text-muted mb-3 block">
              The Reality in India
            </span>
            <h2 className="text-3xl sm:text-4xl lg:text-[56px] font-medium leading-[1.1] tracking-[-0.03em] text-ink mb-4">
              Over 100,000 cybercrimes against women are reported every year.
            </h2>
            <p className="text-base text-body leading-relaxed">
              When private or manipulated images are circulated online without consent, victims face emotional trauma
              compounded by structural, technical, and procedural barriers.
            </p>
          </div>

          {/* 5 Cycling Feature Cards Grid (3-up desktop, 2-up tablet, 1-up mobile) */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Card 1: Pink */}
            <FeatureCard
              color="pink"
              title="1. Uncontrolled Circulation"
              description="Images are downloaded, cropped, flipped, compressed into stickers, and re-uploaded across Telegram channels, Reddit forums, and social feeds within minutes."
              badge="Viral Velocity"
              icon={<RefreshCw className="w-6 h-6" />}
            />

            {/* Card 2: Teal */}
            <FeatureCard
              color="teal"
              title="2. Blind Discovery"
              description="Victims rarely know where their media has spread until alerted by friends or blackmailers. Searching manual platforms is re-traumatizing and incomplete."
              badge="Hidden Exposure"
              icon={<Search className="w-6 h-6" />}
            />

            {/* Card 3: Lavender */}
            <FeatureCard
              color="lavender"
              title="3. Exhausting Repeated Reporting"
              description="Reporting each URL individually through opaque help centers requires filling dozens of separate forms, repeating traumatic details every time."
              badge="Reporting Fatigue"
              icon={<Clock className="w-6 h-6" />}
            />

            {/* Card 4: Peach */}
            <FeatureCard
              color="peach"
              title="4. Vanishing Digital Evidence"
              description="Users fail to preserve cryptographic hashes, UTC timestamps, and tamper-proof logs required by cyber cells, making legal prosecution difficult."
              badge="Legal Vulnerability"
              icon={<FileCheck2 className="w-6 h-6" />}
            />

            {/* Card 5: Ochre */}
            <FeatureCard
              color="ochre"
              title="5. Complex Complaint Procedures"
              description="Navigating cybercrime.gov.in, police stations, IT Act sections (66E, 67A), and platform escalation paths is intimidating without technical guidance."
              badge="Procedural Hurdles"
              icon={<Scale className="w-6 h-6" />}
            />

            {/* Card 6: Cream (SafeTrace Answer) */}
            <FeatureCard
              color="cream"
              title="The SafeTrace Shield"
              description="A single privacy-first workspace that solves all five pain points: automated hashing, multi-platform discovery, verified evidence chains, and one-click bulk reporting."
              badge="Sanctuary Solution"
              icon={<Shield className="w-6 h-6 text-brand-pink" />}
            >
              <Link href="/auth/register" className="inline-flex items-center text-xs font-semibold text-brand-pink hover:underline">
                Start Protected Case →
              </Link>
            </FeatureCard>
          </div>
        </div>
      </section>

      {/* 3. TECHNOLOGY & HOW IT WORKS (Multi-Method Matching & Cryptographic Chain) */}
      <section id="solution" className="py-24 px-6 md:px-12 bg-canvas border-t border-hairline">
        <div className="max-w-container mx-auto">
          <div className="max-w-2xl mb-16">
            <span className="text-xs font-semibold uppercase tracking-wider text-muted mb-3 block">
              Engineered for Dignity
            </span>
            <h2 className="text-3xl sm:text-4xl lg:text-[40px] font-medium leading-[1.1] tracking-[-0.025em] text-ink mb-4">
              State-of-the-art computer vision meets tamper-evident cryptographic law.
            </h2>
            <p className="text-base text-body leading-relaxed">
              SafeTrace operates on a zero-knowledge principle: your intimate media is analyzed in memory to produce
              mathematical hashes, after which raw files are permanently purged.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Feature 1: Multi-Method Perceptual Hashing */}
            <ProductMockupCard>
              <div className="w-10 h-10 rounded-md bg-brand-pink/15 text-brand-pink flex items-center justify-center mb-6">
                <Fingerprint className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-semibold text-ink mb-2">Multi-Method Perceptual Hashes</h3>
              <p className="text-xs text-muted leading-relaxed mb-6">
                Unlike simple SHA-256 that breaks if a single pixel changes, SafeTrace combines:
              </p>
              <ul className="space-y-2 text-xs text-body border-t border-hairline pt-4">
                <li className="flex items-center justify-between py-1">
                  <span className="font-medium">PDQ 256-bit Vector</span>
                  <span className="text-muted text-[11px]">Resistant to filters & compressions</span>
                </li>
                <li className="flex items-center justify-between py-1">
                  <span className="font-medium">Multi-Scale pHash</span>
                  <span className="text-muted text-[11px]">Detects tight crops & aspect ratio shifts</span>
                </li>
                <li className="flex items-center justify-between py-1">
                  <span className="font-medium">ORB Invariant Inliers</span>
                  <span className="text-muted text-[11px]">Keypoint geometry verification</span>
                </li>
                <li className="flex items-center justify-between py-1">
                  <span className="font-medium">SHA-256 Bitwise</span>
                  <span className="text-muted text-[11px]">100% exact copy verification</span>
                </li>
              </ul>
            </ProductMockupCard>

            {/* Feature 2: Tamper-Evident Hash Chain */}
            <ProductMockupCard>
              <div className="w-10 h-10 rounded-md bg-brand-teal/15 text-brand-teal flex items-center justify-center mb-6">
                <LinkIcon className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-semibold text-ink mb-2">Cryptographic Hash Chain</h3>
              <p className="text-xs text-muted leading-relaxed mb-6">
                Every confirmed violation is recorded into an append-only cryptographic ledger with a block sequence:
              </p>
              <div className="bg-surface-card border border-hairline rounded-md p-3 font-mono text-[11px] space-y-2 text-body mb-4">
                <div className="flex justify-between text-muted text-[10px]">
                  <span>BLOCK #0001</span>
                  <span className="text-success font-semibold">VERIFIED</span>
                </div>
                <div className="truncate text-[10px] text-muted">PREV: 0000000000000000000000...</div>
                <div className="truncate font-semibold text-ink">HASH: 7f83b1657ff1fc53b92dc181...</div>
                <div className="text-[10px] text-muted">TIMESTAMP: 2026-11-21T18:24:00Z</div>
              </div>
              <p className="text-[11px] text-muted">
                Meets Indian Evidence Act Section 65B requirements for electronic court admissibility.
              </p>
            </ProductMockupCard>

            {/* Feature 3: Automated Statutory PDF Dossiers */}
            <ProductMockupCard>
              <div className="w-10 h-10 rounded-md bg-brand-ochre/20 text-amber-800 flex items-center justify-center mb-6">
                <FileCheck2 className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-semibold text-ink mb-2">Statutory PDF Dossiers</h3>
              <p className="text-xs text-muted leading-relaxed mb-6">
                One click generates a legal complaint mapped directly to Indian statutory provisions:
              </p>
              <ul className="space-y-2 text-xs text-body border-t border-hairline pt-4">
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-brand-pink" />
                  <span>IT Act 2000 — Section 66E (Privacy Violation)</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-brand-pink" />
                  <span>IT Act 2000 — Section 67 & 67A (Sexually Explicit Content)</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-brand-pink" />
                  <span>IT Rules 2021 — Rule 3(2)(b) (24-Hour Mandatory Takedown)</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-brand-pink" />
                  <span>Bharatiya Nyaya Sanhita — Sections 354C & 354D (Voyeurism & Stalking)</span>
                </li>
              </ul>
            </ProductMockupCard>
          </div>
        </div>
      </section>

      {/* 4. TESTIMONIALS */}
      <section className="py-24 px-6 md:px-12 bg-surface-soft border-t border-hairline">
        <div className="max-w-container mx-auto">
          <div className="text-center max-w-xl mx-auto mb-16">
            <h2 className="text-3xl font-medium text-ink mb-3">Trusted by Advocates & Cyber Counsel</h2>
            <p className="text-sm text-muted">
              Built in consultation with digital rights activists, survivor advocates, and cybercrime defense attorneys.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <TestimonialCard
              quote="SafeTrace solves the biggest hurdle in cybercrime complaints: preserving cryptographic hashes without revictimizing the client by forwarding images around."
              author="Adv. Priya Sharma"
              role="Cyber Crime Advocate, High Court"
            />
            <TestimonialCard
              quote="The 24-hour IT Rule 3(2)(b) notice generator cut our NGO intake processing from four days to under twenty minutes. It gives agency back to survivors."
              author="Dr. Ananya Roy"
              role="Director, Women's Digital Safety Forum"
            />
            <TestimonialCard
              quote="The continuous Celery Beat monitoring caught a deleted image being re-uploaded three weeks later, alerting us to file a contempt escalation immediately."
              author="Meera Nair"
              role="Legal Aid Counselor"
            />
          </div>
        </div>
      </section>

      {/* 5. PRICING & TIERS */}
      <section className="py-24 px-6 md:px-12 bg-canvas border-t border-hairline">
        <div className="max-w-container mx-auto">
          <div className="text-center max-w-xl mx-auto mb-16">
            <h2 className="text-3xl font-medium text-ink mb-3">Free for Every Survivor</h2>
            <p className="text-sm text-muted">
              Victims never pay to defend their dignity. Enterprise and institutional plans support our free public
              mission.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <PricingTierCard
              title="Survivor Sanctuary"
              price="₹0"
              billingPeriod="forever free"
              description="For individual victims seeking immediate image protection and evidence documentation."
              features={[
                "Unlimited zero-knowledge fingerprints",
                "Automated discovery across 6 platforms",
                "Human-in-the-loop verification",
                "Tamper-evident evidence chain ledger",
                "ReportLab PDF legal complaint dossiers",
                "24/7 Celery Beat URL liveness scans",
              ]}
              ctaText="Create Protected Case"
              ctaHref="/auth/register"
            />

            <PricingTierCard
              title="Advocate & NGO"
              price="₹2,499"
              billingPeriod="/month (or grant subsidized)"
              description="For legal aid clinics, NGOs, and counselors managing multiple client cases simultaneously."
              features={[
                "Everything in Survivor, plus:",
                "Multi-client case management",
                "Consolidated statutory filing bundles",
                "Priority discovery background workers",
                "Client pseudonymity management",
                "Audit log export for court affidavits",
              ]}
              isFeatured={true}
              ctaText="Start NGO Workspace"
              ctaHref="/auth/register?role=NGO"
            />

            <PricingTierCard
              title="Institutional"
              price="Custom"
              billingPeriod="annual partnership"
              description="For universities, platforms, and law enforcement agencies requiring on-premise deployments."
              features={[
                "Private VPC / On-Premise Docker cluster",
                "Custom PlatformConnector integrations",
                "Direct Law Enforcement portal bridges",
                "SLA & Dedicated Trust & Safety Architect",
                "Air-gapped database deployment",
              ]}
              ctaText="Contact Safety Architects"
              ctaHref="/resources"
            />
          </div>
        </div>
      </section>

      {/* 6. CTA BAND (Surface-soft, radius xl, padding 80, display-md heading + primary button) */}
      <section className="py-16 px-6 md:px-12 bg-canvas">
        <div className="max-w-container mx-auto bg-surface-soft border border-hairline rounded-xl p-12 md:p-20 flex flex-col md:flex-row items-center justify-between gap-12">
          <div className="max-w-xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-pill bg-canvas text-ink text-xs font-medium border border-hairline mb-4">
              <Lock className="w-3.5 h-3.5 text-brand-teal" />
              <span>Your privacy is mathematically protected</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-medium text-ink tracking-tight mb-4">
              Take the first step in total privacy.
            </h2>
            <p className="text-sm text-body leading-relaxed mb-6">
              You do not need to provide your real name, phone number, or government ID to compute perceptual hashes.
              Begin building your verified evidence dossier today.
            </p>
            <div className="flex flex-wrap items-center gap-4">
              <Link href="/auth/register">
                <Button size="lg" rightIcon={<ArrowRight className="w-4 h-4" />}>
                  Create Anonymous Case
                </Button>
              </Link>
              <Link href="/resources">
                <Button variant="secondary" size="lg">
                  Emergency Helplines (1930 / 181)
                </Button>
              </Link>
            </div>
          </div>
          <div className="w-48 h-48 flex-shrink-0">
            <SecurityShieldClay className="w-full h-full" />
          </div>
        </div>
      </section>
    </div>
  );
}
