"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Shield, Menu, X, User as UserIcon, LogOut } from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { QuickExit } from "./QuickExit";

export function TopNav() {
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="h-[64px] bg-canvas border-b border-hairline sticky top-0 z-50 px-4 md:px-8">
      <div className="max-w-container mx-auto h-full flex items-center justify-between">
        {/* Left: Brand Logo */}
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-9 h-9 rounded-md bg-brand-pink text-white flex items-center justify-center font-bold shadow-sm transition-transform group-hover:scale-105">
            <Shield className="w-5 h-5 fill-white stroke-brand-pink" />
          </div>
          <span className="font-display font-medium text-xl text-ink tracking-tight">SafeTrace</span>
        </Link>

        {/* Center: Navigation Links (Desktop) */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-body">
          <Link href="/#problem" className="hover:text-ink transition-colors">
            Problem
          </Link>
          <Link href="/#solution" className="hover:text-ink transition-colors">
            Technology
          </Link>
          <Link href="/resources" className="hover:text-ink transition-colors">
            Helplines & Resources
          </Link>
          <Link href="/plans" className="hover:text-ink transition-colors">
            Pricing
          </Link>
          {user && (
            <Link href="/dashboard" className="text-ink font-semibold border-b-2 border-brand-pink pb-0.5">
              Dashboard
            </Link>
          )}
        </nav>

        {/* Right: Quick Exit + Auth Actions */}
        <div className="flex items-center gap-3">
          {/* Visible Trauma-Informed Quick Exit Button */}
          <QuickExit />

          {/* User state */}
          <div className="hidden sm:flex items-center gap-3">
            {user ? (
              <div className="flex items-center gap-3">
                <Link
                  href="/cases/new"
                  className="h-[38px] px-3.5 bg-ink text-white text-xs font-semibold rounded-md hover:bg-neutral-800 transition-colors flex items-center min-h-[38px]"
                >
                  New Case
                </Link>
                <div className="flex items-center gap-2 pl-2 border-l border-hairline">
                  <span className="text-xs font-medium text-ink bg-surface-card px-2.5 py-1 rounded-pill flex items-center gap-1.5 border border-hairline">
                    <UserIcon className="w-3.5 h-3.5 text-muted" />
                    <span className="max-w-[120px] truncate">{user.full_name || user.email}</span>
                  </span>
                  <button
                    onClick={logout}
                    title="Sign Out"
                    className="p-1.5 text-muted hover:text-ink rounded-md transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-4">
                <Link href="/auth/login" className="text-sm font-medium text-ink hover:text-muted transition-colors">
                  Sign in
                </Link>
                <Link
                  href="/auth/register"
                  className="h-[40px] px-4 bg-ink text-white text-xs font-semibold rounded-md hover:bg-neutral-800 transition-colors flex items-center min-h-[40px]"
                >
                  Protect Your Images
                </Link>
              </div>
            )}
          </div>

          {/* Mobile hamburger button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 text-ink rounded-md hover:bg-surface-soft"
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-canvas border-b border-hairline px-6 py-5 flex flex-col gap-4 text-sm font-medium shadow-md">
          <Link href="/#problem" onClick={() => setMobileMenuOpen(false)}>
            Problem
          </Link>
          <Link href="/#solution" onClick={() => setMobileMenuOpen(false)}>
            Technology
          </Link>
          <Link href="/resources" onClick={() => setMobileMenuOpen(false)}>
            Helplines & Official Resources
          </Link>
          <Link href="/plans" onClick={() => setMobileMenuOpen(false)}>
            Pricing & Plans
          </Link>
          {user ? (
            <>
              <Link
                href="/dashboard"
                onClick={() => setMobileMenuOpen(false)}
                className="font-semibold text-brand-pink"
              >
                Go to Dashboard
              </Link>
              <Link
                href="/cases/new"
                onClick={() => setMobileMenuOpen(false)}
                className="font-semibold text-ink"
              >
                + Create New Case
              </Link>
              <button
                onClick={() => {
                  logout();
                  setMobileMenuOpen(false);
                }}
                className="text-left text-error font-medium"
              >
                Sign Out
              </button>
            </>
          ) : (
            <div className="pt-2 border-t border-hairline flex flex-col gap-2">
              <Link
                href="/auth/login"
                onClick={() => setMobileMenuOpen(false)}
                className="text-center py-2 rounded-md border border-hairline"
              >
                Sign In
              </Link>
              <Link
                href="/auth/register"
                onClick={() => setMobileMenuOpen(false)}
                className="text-center py-2 bg-ink text-white rounded-md"
              >
                Register Anonymously
              </Link>
            </div>
          )}
        </div>
      )}
    </header>
  );
}
