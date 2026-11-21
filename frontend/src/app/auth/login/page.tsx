"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Shield, Lock, ArrowRight, Sparkles, AlertCircle } from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/Button";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      await login(email, password);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Failed to log in. Please check your credentials.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoFill = () => {
    setEmail("victim@example.com");
    setPassword("VictimPass123!");
    setError(null);
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center p-6 bg-canvas">
      <div className="w-full max-w-md">
        {/* Card Header */}
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-xl bg-brand-pink text-white flex items-center justify-center mx-auto mb-4 shadow-sm">
            <Shield className="w-6 h-6 fill-white stroke-brand-pink" />
          </div>
          <h1 className="text-2xl font-medium text-ink tracking-tight mb-2">Welcome to SafeTrace</h1>
          <p className="text-sm text-muted">
            Access your secure cases, verified evidence vaults, and takedown tracking.
          </p>
        </div>

        {/* Demo Credentials Quick Pill */}
        <div className="bg-surface-card border border-hairline rounded-lg p-3.5 mb-6 flex items-center justify-between text-xs">
          <div className="flex items-center gap-2 text-body">
            <Sparkles className="w-4 h-4 text-brand-pink flex-shrink-0" />
            <span>Hackathon Judge / Demo Evaluator?</span>
          </div>
          <button
            type="button"
            onClick={handleDemoFill}
            className="px-2.5 py-1 bg-ink text-white font-medium rounded-sm text-[11px] hover:bg-neutral-800 transition-colors"
          >
            Quick Fill Demo
          </button>
        </div>

        {/* Form Card */}
        <div className="bg-canvas border border-hairline rounded-xl p-8 shadow-sm">
          {error && (
            <div className="mb-6 p-3 rounded-md bg-error/10 border border-error/20 flex items-start gap-2.5 text-xs text-error">
              <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-xs font-semibold text-ink uppercase tracking-wider mb-2">
                Email / Pseudonym
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@domain.com"
                className="w-full h-[44px] px-4 rounded-md bg-canvas border border-hairline text-ink text-sm focus:outline-none focus:border-ink transition-colors"
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-semibold text-ink uppercase tracking-wider">
                  Password
                </label>
              </div>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full h-[44px] px-4 rounded-md bg-canvas border border-hairline text-ink text-sm focus:outline-none focus:border-ink transition-colors"
              />
            </div>

            <Button type="submit" size="lg" className="w-full" isLoading={isLoading} rightIcon={<ArrowRight className="w-4 h-4" />}>
              Sign In Securely
            </Button>
          </form>

          <div className="mt-6 pt-6 border-t border-hairline text-center text-xs text-muted">
            Don't have a case yet?{" "}
            <Link href="/auth/register" className="font-semibold text-ink hover:underline">
              Register anonymously
            </Link>
          </div>
        </div>

        {/* Trust Note */}
        <div className="mt-8 text-center text-[11px] text-muted-soft flex items-center justify-center gap-1.5">
          <Lock className="w-3.5 h-3.5" />
          <span>All sessions use secure Argon2id & cryptographic tokens</span>
        </div>
      </div>
    </div>
  );
}
