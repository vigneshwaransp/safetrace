import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/lib/auth-context";
import { TopNav } from "@/components/TopNav";
import { Footer } from "@/components/Footer";

export const metadata: Metadata = {
  title: "SafeTrace | Non-Consensual Image Abuse Prevention & Evidence Management",
  description:
    "A victim-centric, trauma-informed digital platform helping survivors of non-consensual image abuse fingerprint media, identify unauthorized copies, safeguard tamper-evident evidence, and streamline takedown reporting.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-canvas text-body-strong antialiased selection:bg-brand-lavender selection:text-ink min-h-screen flex flex-col">
        <AuthProvider>
          <TopNav />
          <main className="flex-1">{children}</main>
          <Footer />
        </AuthProvider>
      </body>
    </html>
  );
}
