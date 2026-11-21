"use client";

import React, { Suspense, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Shield, Lock, ArrowRight, Check, AlertCircle, RefreshCw } from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/Button";

function RegisterForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const defaultRole = searchParams.get("role") || "VICTIM";

  const { register } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [role, setRole] = useState(defaultRole);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      await register(email, password, fullName || undefined, role);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Failed to create account. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-canvas border border-hairline rounded-xl p-8 shadow-sm">
      {error && (
        <div className="mb-6 p-3 rounded-md bg-error/10 border border-error/20 flex items-start gap-2.5 text-xs text-error">
          <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5">
        {/* Role Selection Tabs */}
        <div>
          <label className="block text-xs font-semibold text-ink uppercase tracking-wider mb-2">
            I am registering as:
          </label>
          <div className="grid grid-cols-3 gap-2">
            {[
              { id: "VICTIM", label: "Survivor" },
              { id: "ADVOCATE", label: "Legal Advocate" },
              { id: "NGO", label: "NGO / Counselor" },
            ].map((item) => (
              <button
                key={item.id}
                type="button"
                onClick={() => setRole(item.id)}
                className={`h-[40px] text-xs font-medium rounded-md border transition-all flex items-center justify-center gap-1.5 ${
                  role === item.id
                    ? "bg-surface-card border-ink text-ink font-semibold"
                    : "bg-canvas border-hairline text-muted hover:bg-surface-soft"
                }`}
              >
                {role === item.id && <Check className="w-3.5 h-3.5 text-brand-pink" />}
                <span>{item.label}</span>
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold text-ink uppercase tracking-wider mb-2">
            Display Name or Pseudonym (Optional)
          </label>
          <input
            type="text"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            placeholder="e.g. Maya or Anonymous Survivor"
            className="w-full h-[44px] px-4 rounded-md bg-canvas border border-hairline text-ink text-sm focus:outline-none focus:border-ink transition-colors"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-ink uppercase tracking-wider mb-2">
            Email Address
          </label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="safe-email@domain.com"
            className="w-full h-[44px] px-4 rounded-md bg-canvas border border-hairline text-ink text-sm focus:outline-none focus:border-ink transition-colors"
          />
          <p className="text-[11px] text-muted-soft mt-1">
            Used only for encrypted login and takedown notifications. Never shared or sold.
          </p>
        </div>

        <div>
          <label className="block text-xs font-semibold text-ink uppercase tracking-wider mb-2">
            Master Password
          </label>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="At least 8 characters"
            minLength={8}
            className="w-full h-[44px] px-4 rounded-md bg-canvas border border-hairline text-ink text-sm focus:outline-none focus:border-ink transition-colors"
          />
        </div>

        <Button type="submit" size="lg" className="w-full" isLoading={isLoading} rightIcon={<ArrowRight className="w-4 h-4" />}>
          Create Protected Case Workspace
        </Button>
      </form>

      <div className="mt-6 pt-6 border-t border-hairline text-center text-xs text-muted">
        Already registered?{" "}
        <Link href="/auth/login" className="font-semibold text-ink hover:underline">
          Sign in to your case
        </Link>
      </div>
    </div>
  );
}

export default function RegisterPage() {
  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center p-6 bg-canvas">
      <div className="w-full max-w-lg">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-xl bg-brand-pink text-white flex items-center justify-center mx-auto mb-4 shadow-sm">
            <Shield className="w-6 h-6 fill-white stroke-brand-pink" />
          </div>
          <h1 className="text-2xl font-medium text-ink tracking-tight mb-2">Create a Safe Space</h1>
          <p className="text-sm text-muted">
            You may register pseudononymously. Real name and phone numbers are completely optional.
          </p>
        </div>

        <Suspense
          fallback={
            <div className="bg-canvas border border-hairline rounded-xl p-12 text-center text-sm text-muted flex items-center justify-center gap-2">
              <RefreshCw className="w-4 h-4 animate-spin text-brand-pink" />
              <span>Loading registration form...</span>
            </div>
          }
        >
          <RegisterForm />
        </Suspense>

        <div className="mt-8 text-center text-[11px] text-muted-soft flex items-center justify-center gap-1.5">
          <Lock className="w-3.5 h-3.5" />
          <span>Compliant with Indian DPDP Act 2023 principles of purpose limitation</span>
        </div>
      </div>
    </div>
  );
}
