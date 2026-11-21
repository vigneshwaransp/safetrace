import React from "react";
import Link from "next/link";
import { Shield, PhoneCall, ExternalLink, HeartHandshake } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-surface-soft border-t border-hairline py-20 px-6 md:px-12 text-sm text-body">
      <div className="max-w-container mx-auto">
        {/* Helplines Emergency Banner */}
        <div className="bg-surface-card border border-hairline rounded-xl p-6 mb-16 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-brand-pink/15 text-brand-pink flex items-center justify-center flex-shrink-0">
              <PhoneCall className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-semibold text-ink text-sm">Emergency & Immediate Assistance</h4>
              <p className="text-xs text-muted">
                If you are in immediate danger or facing extortion, reach verified 24/7 national helplines immediately.
              </p>
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-3 text-xs font-semibold">
            <a
              href="tel:1930"
              className="px-4 py-2 bg-ink text-white rounded-md hover:bg-neutral-800 transition-colors"
            >
              Cybercrime: 1930
            </a>
            <a
              href="tel:181"
              className="px-4 py-2 bg-surface-strong border border-hairline text-ink rounded-md hover:bg-surface-soft transition-colors"
            >
              Women Helpline: 181
            </a>
            <a
              href="tel:+917827170170"
              className="px-4 py-2 bg-surface-strong border border-hairline text-ink rounded-md hover:bg-surface-soft transition-colors"
            >
              NCW: 7827-170-170
            </a>
          </div>
        </div>

        {/* 4-Column Link Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-12 mb-16">
          {/* Col 1: SafeTrace Mission */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-7 h-7 rounded-md bg-brand-pink text-white flex items-center justify-center font-bold">
                <Shield className="w-4 h-4 fill-white stroke-brand-pink" />
              </div>
              <span className="font-display font-medium text-lg text-ink">SafeTrace</span>
            </div>
            <p className="text-xs text-muted leading-relaxed mb-4">
              A victim-centric, trauma-informed digital sanctuary empowering survivors of non-consensual image abuse to
              safeguard evidence, automate takedown requests, and regain digital sovereignty.
            </p>
            <div className="inline-flex items-center gap-1.5 text-xs text-brand-teal font-medium">
              <HeartHandshake className="w-4 h-4" />
              <span>Built for K-Hacks 4.0</span>
            </div>
          </div>

          {/* Col 2: Platform & Features */}
          <div>
            <h5 className="font-semibold text-ink text-xs uppercase tracking-wider mb-4">Capabilities</h5>
            <ul className="space-y-2.5 text-xs">
              <li>
                <Link href="/#solution" className="hover:text-ink transition-colors">
                  Zero-Knowledge Fingerprinting
                </Link>
              </li>
              <li>
                <Link href="/#solution" className="hover:text-ink transition-colors">
                  Multi-Platform Discovery
                </Link>
              </li>
              <li>
                <Link href="/#solution" className="hover:text-ink transition-colors">
                  Tamper-Evident Hash Chains
                </Link>
              </li>
              <li>
                <Link href="/#solution" className="hover:text-ink transition-colors">
                  ReportLab PDF Legal Dossiers
                </Link>
              </li>
              <li>
                <Link href="/#solution" className="hover:text-ink transition-colors">
                  24/7 Celery Beat Monitoring
                </Link>
              </li>
            </ul>
          </div>

          {/* Col 3: Official Support & Channels */}
          <div>
            <h5 className="font-semibold text-ink text-xs uppercase tracking-wider mb-4">Official Channels</h5>
            <ul className="space-y-2.5 text-xs">
              <li>
                <a
                  href="https://cybercrime.gov.in"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1 hover:text-ink transition-colors"
                >
                  <span>National Cyber Crime Portal</span>
                  <ExternalLink className="w-3 h-3 text-muted-soft" />
                </a>
              </li>
              <li>
                <a
                  href="https://stopncii.org"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1 hover:text-ink transition-colors"
                >
                  <span>StopNCII.org (Adults)</span>
                  <ExternalLink className="w-3 h-3 text-muted-soft" />
                </a>
              </li>
              <li>
                <a
                  href="https://takeitdown.ncmec.org"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1 hover:text-ink transition-colors"
                >
                  <span>Take It Down (Under 18)</span>
                  <ExternalLink className="w-3 h-3 text-muted-soft" />
                </a>
              </li>
              <li>
                <a
                  href="http://ncw.nic.in"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1 hover:text-ink transition-colors"
                >
                  <span>National Commission for Women</span>
                  <ExternalLink className="w-3 h-3 text-muted-soft" />
                </a>
              </li>
              <li>
                <Link href="/resources" className="text-brand-pink font-medium hover:underline">
                  View Full Guidance Directory →
                </Link>
              </li>
            </ul>
          </div>

          {/* Col 4: Trust, Safety & Ethics */}
          <div>
            <h5 className="font-semibold text-ink text-xs uppercase tracking-wider mb-4">Trust & Ethics</h5>
            <ul className="space-y-2.5 text-xs">
              <li>
                <Link href="/settings" className="hover:text-ink transition-colors">
                  Zero-Storage Guarantee
                </Link>
              </li>
              <li>
                <Link href="/settings" className="hover:text-ink transition-colors">
                  One-Click Data Purge
                </Link>
              </li>
              <li>
                <Link href="/plans" className="hover:text-ink transition-colors">
                  NGO & Advocate Licensing
                </Link>
              </li>
              <li>
                <span className="text-muted-soft">ISO / IT Act 66E Compliant Format</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Legal Disclaimer & Copyright */}
        <div className="pt-8 border-t border-hairline flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-muted">
          <p>© {new Date().getFullYear()} SafeTrace. Dedicated to survivor dignity, privacy, and safety.</p>
          <p className="text-[11px] max-w-xl text-center md:text-right">
            Disclaimer: SafeTrace assists in evidence preservation and complaint generation. We do not provide legal
            representation or auto-file police complaints without verified user consent.
          </p>
        </div>
      </div>
    </footer>
  );
}
