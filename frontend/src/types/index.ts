export type UserRole = "VICTIM" | "ADVOCATE" | "NGO" | "ADMIN";

export interface User {
  id: string;
  email: string;
  full_name?: string | null;
  role: UserRole;
  organization?: string | null;
  is_active: boolean;
  created_at: string;
}

export type CaseStatus = "OPEN" | "DISCOVERY_RUNNING" | "EVIDENCE_COLLECTED" | "REPORTED" | "RESOLVED" | "CLOSED";

export interface Case {
  id: string;
  user_id: string;
  case_number: string;
  title: string;
  incident_date?: string | null;
  summary?: string | null;
  suspected_platforms?: string[] | null;
  target_urls?: string[] | null;
  status: CaseStatus;
  is_anonymous: boolean;
  retain_encrypted_files: boolean;
  created_at: string;
  updated_at: string;
  images_count?: number;
  matches_count?: number;
  evidence_count?: number;
}

export interface CaseImage {
  id: string;
  case_id: string;
  original_filename: string;
  content_type: string;
  file_size_bytes: number;
  sha256: string;
  pdq_hash?: string | null;
  pdq_quality?: number | null;
  phash?: string | null;
  dhash?: string | null;
  ahash?: string | null;
  is_original_deleted: boolean;
  created_at: string;
}

export type JobStatus = "PENDING" | "RUNNING" | "COMPLETED" | "FAILED";

export interface DiscoveryJob {
  id: string;
  case_id: string;
  connector_type: string;
  status: JobStatus;
  items_scanned: number;
  matches_found: number;
  started_at?: string | null;
  completed_at?: string | null;
  error_message?: string | null;
  created_at: string;
}

export type MatchStatus = "PENDING_REVIEW" | "CONFIRMED" | "REJECTED" | "UNSURE";
export type MatchConfidence = "HIGH" | "MEDIUM" | "LOW" | "NONE";

export interface Match {
  id: string;
  case_id: string;
  case_image_id: string;
  discovery_job_id?: string | null;
  platform: string;
  source_url: string;
  thumbnail_url?: string | null;
  author_handle?: string | null;
  post_timestamp?: string | null;
  similarity_score: number;
  confidence: MatchConfidence;
  distance_pdq?: number | null;
  distance_phash?: number | null;
  sha256_match: boolean;
  matching_reasons?: string[] | null;
  status: MatchStatus;
  reviewer_notes?: string | null;
  reviewed_at?: string | null;
  created_at: string;
}

export interface EvidenceItem {
  id: string;
  case_id: string;
  match_id: string;
  evidence_number: string;
  platform: string;
  source_url: string;
  captured_sha256: string;
  similarity_score: number;
  confidence: MatchConfidence;
  author_handle?: string | null;
  post_timestamp?: string | null;
  captured_at: string;
  previous_evidence_hash?: string | null;
  evidence_hash: string;
  chain_sequence: number;
  is_verified?: boolean;
}

export type ReportStatus = "DRAFT" | "SUBMITTED" | "ACKNOWLEDGED" | "REMOVED" | "REJECTED" | "REAPPEARED";

export interface Report {
  id: string;
  case_id: string;
  platform: string;
  status: ReportStatus;
  selected_evidence_ids: string[];
  report_text: string;
  platform_ticket_id?: string | null;
  submission_url?: string | null;
  statutory_basis?: string[] | null;
  has_pdf: boolean;
  pdf_filename?: string | null;
  last_monitored_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ReportStatusHistory {
  id: string;
  report_id: string;
  previous_status?: ReportStatus | null;
  new_status: ReportStatus;
  notes?: string | null;
  created_at: string;
}

export interface Notification {
  id: string;
  user_id: string;
  case_id?: string | null;
  report_id?: string | null;
  title: string;
  message: string;
  category: "REMOVAL_CONFIRMED" | "REAPPEARED" | "MATCH_FOUND" | "SYSTEM";
  is_read: boolean;
  created_at: string;
}

export interface OfficialChannel {
  name: string;
  description: string;
  contact: string;
  url: string;
  guidelines: string[];
  mandatory_evidence: string[];
  turnaround_expectation: string;
}
