import uuid
from datetime import datetime, timezone
from typing import List, Optional, Any
from sqlalchemy import String, DateTime, Uuid, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    case_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("cases.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    report_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )  # e.g., REP-2026-0001
    report_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )  # PLATFORM_TAKEDOWN, CYBERCRIME_GOV, POLICE_COMPLAINT, NGO_SUBMISSION
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    recipient_platform: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    selected_evidence_ids: Mapped[Any] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )
    report_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    pdf_storage_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="DRAFT",
        nullable=False
    )  # DRAFT, SUBMITTED, ACKNOWLEDGED, REMOVED, REJECTED, REAPPEARED
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    case: Mapped["Case"] = relationship(
        "Case",
        back_populates="reports"
    )
    status_history: Mapped[List["ReportStatusHistory"]] = relationship(
        "ReportStatusHistory",
        back_populates="report",
        cascade="all, delete-orphan",
        order_by="ReportStatusHistory.created_at.desc()"
    )


class ReportStatusHistory(Base):
    __tablename__ = "report_status_history"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    report_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("reports.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    previous_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    new_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    changed_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    report: Mapped["Report"] = relationship(
        "Report",
        back_populates="status_history"
    )
