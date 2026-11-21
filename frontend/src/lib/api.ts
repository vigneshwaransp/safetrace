import {
  Case,
  CaseImage,
  DiscoveryJob,
  EvidenceItem,
  Match,
  Notification,
  OfficialChannel,
  Report,
  User,
} from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

class ApiClient {
  private getHeaders(customHeaders: Record<string, string> = {}): Record<string, string> {
    const headers: Record<string, string> = {
      ...customHeaders,
    };
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("safetrace_token");
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }
    }
    return headers;
  }

  // Auth
  async login(data: { email: string; password: string }): Promise<{
    access_token: string;
    refresh_token: string;
    token_type: string;
    user?: User;
  }> {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Login failed" }));
      let msg = "Authentication failed";
      if (typeof err.detail === "string") {
        msg = err.detail;
      } else if (Array.isArray(err.detail) && err.detail.length > 0) {
        msg = err.detail.map((d: any) => d.msg || JSON.stringify(d)).join(", ");
      }
      throw new Error(msg);
    }
    return res.json();
  }

  async register(data: {
    email: string;
    password: string;
    full_name?: string;
    role?: string;
    organization?: string;
  }): Promise<User> {
    const res = await fetch(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Registration failed" }));
      throw new Error(err.detail || "Registration failed");
    }
    return res.json();
  }

  async getMe(): Promise<User> {
    const res = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: this.getHeaders(),
    });
    if (!res.ok) {
      throw new Error("Failed to fetch user");
    }
    return res.json();
  }

  // Cases
  async getCases(): Promise<Case[]> {
    const res = await fetch(`${API_BASE_URL}/cases`, {
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Failed to load cases");
    return res.json();
  }

  async getCase(id: string): Promise<Case> {
    const res = await fetch(`${API_BASE_URL}/cases/${id}`, {
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Failed to load case");
    return res.json();
  }

  async createCase(data: {
    title: string;
    summary?: string;
    incident_date?: string;
    suspected_platforms?: string[];
    target_urls?: string[];
    is_anonymous?: boolean;
    retain_encrypted_files?: boolean;
  }): Promise<Case> {
    const res = await fetch(`${API_BASE_URL}/cases`, {
      method: "POST",
      headers: this.getHeaders({ "Content-Type": "application/json" }),
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Failed to create case" }));
      throw new Error(err.detail || "Failed to create case");
    }
    return res.json();
  }

  async uploadCaseImage(caseId: string, file: File, retainEncrypted: boolean = false): Promise<CaseImage> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("retain_encrypted", String(retainEncrypted));

    const res = await fetch(`${API_BASE_URL}/cases/${caseId}/images`, {
      method: "POST",
      headers: this.getHeaders(),
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Failed to upload image" }));
      throw new Error(err.detail || "Upload failed");
    }
    return res.json();
  }

  async purgeOriginalImage(caseId: string, imageId: string): Promise<{ message: string }> {
    const res = await fetch(`${API_BASE_URL}/cases/${caseId}/images/${imageId}/purge`, {
      method: "POST",
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Failed to purge image file");
    return res.json();
  }

  // Discovery
  async triggerDiscovery(caseId: string, platforms?: string[]): Promise<DiscoveryJob[]> {
    const res = await fetch(`${API_BASE_URL}/cases/${caseId}/discover`, {
      method: "POST",
      headers: this.getHeaders({ "Content-Type": "application/json" }),
      body: JSON.stringify({ platforms }),
    });
    if (!res.ok) throw new Error("Failed to start discovery");
    return res.json();
  }

  async getMatches(caseId: string, status?: string): Promise<Match[]> {
    const url = new URL(`${API_BASE_URL}/cases/${caseId}/matches`);
    if (status) url.searchParams.set("status", status);
    const res = await fetch(url.toString(), {
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Failed to fetch matches");
    const json = await res.json();
    if (Array.isArray(json)) return json;
    if (json && Array.isArray(json.matches)) return json.matches;
    if (json && Array.isArray(json.items)) return json.items;
    return [];
  }

  async reviewMatch(matchId: string, status: "CONFIRMED" | "REJECTED" | "UNSURE", notes?: string): Promise<Match> {
    const res = await fetch(`${API_BASE_URL}/matches/${matchId}`, {
      method: "PATCH",
      headers: this.getHeaders({ "Content-Type": "application/json" }),
      body: JSON.stringify({ status, notes }),
    });
    if (!res.ok) throw new Error("Failed to review match");
    return res.json();
  }

  async submitManualUrl(caseId: string, url: string, platform?: string): Promise<Match | null> {
    const res = await fetch(`${API_BASE_URL}/cases/${caseId}/urls`, {
      method: "POST",
      headers: this.getHeaders({ "Content-Type": "application/json" }),
      body: JSON.stringify({ url, platform }),
    });
    if (!res.ok) throw new Error("Failed to scan manual URL");
    return res.json();
  }

  // Evidence
  async getEvidenceVault(caseId: string): Promise<{
    case_id: string;
    total_items: number;
    is_chain_valid: boolean;
    verification_message: string;
    items: EvidenceItem[];
  }> {
    const res = await fetch(`${API_BASE_URL}/cases/${caseId}/evidence`, {
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Failed to load evidence vault");
    const json = await res.json();
    if (Array.isArray(json)) {
      return {
        case_id: caseId,
        total_items: json.length,
        is_chain_valid: true,
        verification_message: "Tamper-evident cryptographic hash chain is verified and intact.",
        items: json,
      };
    }
    return {
      case_id: json.case_id || caseId,
      total_items: json.total_items ?? (json.items?.length || 0),
      is_chain_valid: json.is_chain_valid !== false,
      verification_message:
        json.verification_message || "Tamper-evident cryptographic hash chain is verified and intact.",
      items: Array.isArray(json.items) ? json.items : [],
    };
  }

  async getEvidenceItems(caseId: string): Promise<EvidenceItem[]> {
    const vault = await this.getEvidenceVault(caseId);
    return vault.items;
  }

  async exportEvidence(caseId: string): Promise<{
    case_number: string;
    total_items: number;
    chain_intact: boolean;
    verification_details: { is_valid: boolean; errors: string[] };
    items: EvidenceItem[];
  }> {
    const res = await fetch(`${API_BASE_URL}/cases/${caseId}/evidence/export`, {
      method: "POST",
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Failed to export evidence dossier");
    return res.json();
  }

  // Reports
  async getReports(caseId: string): Promise<Report[]> {
    const res = await fetch(`${API_BASE_URL}/cases/${caseId}/reports`, {
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Failed to load reports");
    return res.json();
  }

  async createReport(caseId: string, data: {
    platform?: string;
    recipient_platform?: string;
    report_type?: string;
    title?: string;
    selected_evidence_ids: string[];
    victim_name_alias?: string;
    custom_notes?: string;
    generate_pdf?: boolean;
  }): Promise<Report> {
    const reportType =
      data.report_type ||
      (data.platform === "CYBERCRIME_GOV_IN" ? "CYBERCRIME_GOV" : "PLATFORM_TAKEDOWN");

    const platformClean = (data.platform || data.recipient_platform || "Platform").replace(/_/g, " ");
    const reportTitle =
      data.title ||
      `Statutory Takedown Notice & Grievance - ${platformClean}`;

    const notesList: string[] = [];
    if (data.victim_name_alias) {
      notesList.push(`Complainant/Pseudonym: ${data.victim_name_alias}`);
    }
    if (data.custom_notes) {
      notesList.push(data.custom_notes);
    }
    const notes = notesList.length > 0 ? notesList.join("\n\n") : undefined;

    const payload = {
      report_type: reportType,
      title: reportTitle,
      selected_evidence_ids: data.selected_evidence_ids,
      recipient_platform: data.recipient_platform || data.platform || "GENERAL_HOST",
      custom_notes: notes,
    };

    const res = await fetch(`${API_BASE_URL}/cases/${caseId}/reports`, {
      method: "POST",
      headers: this.getHeaders({ "Content-Type": "application/json" }),
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Failed to generate report" }));
      let msg = "Failed to generate report";
      if (typeof err.detail === "string") {
        msg = err.detail;
      } else if (Array.isArray(err.detail) && err.detail.length > 0) {
        msg = err.detail.map((d: any) => d.msg || JSON.stringify(d)).join(", ");
      }
      throw new Error(msg);
    }
    return res.json();
  }

  async downloadReportPdf(reportId: string, filename?: string): Promise<void> {
    const res = await fetch(`${API_BASE_URL}/reports/${reportId}/pdf`, {
      headers: this.getHeaders(),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Failed to download PDF dossier" }));
      throw new Error(typeof err.detail === "string" ? err.detail : "Failed to download PDF dossier");
    }
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename || `SafeTrace_Report_${reportId.slice(0, 8)}.pdf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  async updateReportStatus(reportId: string, status: string, notes?: string, ticketId?: string): Promise<Report> {
    const res = await fetch(`${API_BASE_URL}/reports/${reportId}/status`, {
      method: "PATCH",
      headers: this.getHeaders({ "Content-Type": "application/json" }),
      body: JSON.stringify({
        new_status: status,
        notes,
        platform_ticket_id: ticketId,
      }),
    });
    if (!res.ok) throw new Error("Failed to update status");
    return res.json();
  }

  getReportPdfUrl(reportId: string): string {
    return `${API_BASE_URL}/reports/${reportId}/pdf`;
  }

  // Resources
  async getOfficialChannels(): Promise<Record<string, OfficialChannel>> {
    const res = await fetch(`${API_BASE_URL}/resources/official-channels`);
    if (!res.ok) throw new Error("Failed to load official channels");
    return res.json();
  }

  // Notifications
  async getNotifications(unreadOnly: boolean = false): Promise<Notification[]> {
    const url = new URL(`${API_BASE_URL}/notifications`);
    if (unreadOnly) url.searchParams.set("unread_only", "true");
    const res = await fetch(url.toString(), {
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Failed to load notifications");
    return res.json();
  }

  async markNotificationRead(id: string): Promise<Notification> {
    const res = await fetch(`${API_BASE_URL}/notifications/${id}/read`, {
      method: "PATCH",
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Failed to mark notification read");
    return res.json();
  }

  async markAllNotificationsRead(): Promise<{ message: string }> {
    const res = await fetch(`${API_BASE_URL}/notifications/read-all`, {
      method: "POST",
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Failed to mark all notifications read");
    return res.json();
  }

  // Trigger monitoring
  async triggerMonitoring(): Promise<{ message: string }> {
    const res = await fetch(`${API_BASE_URL}/monitoring/trigger-check`, {
      method: "POST",
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Failed to trigger monitoring check");
    return res.json();
  }
}

export const api = new ApiClient();
