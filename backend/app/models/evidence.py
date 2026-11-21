import uuid
from datetime import datetime, timezone
from typing import Optional, Any
from sqlalchemy import String, DateTime, Uuid, ForeignKey, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class EvidenceItem(Base):
    __tablename__ = "evidence_items"

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
    match_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("matches.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False
    )
    evidence_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )  # e.g., EV-2026-0001
    platform: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    source_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )
    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    content_sha256: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )
    screenshot_storage_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )
    similarity_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    metadata_snapshot: Mapped[Any] = mapped_column(
        JSON,
        default=dict,
        nullable=False
    )

    # Tamper-Evident Hash Chain
    previous_evidence_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )  # SHA-256 of previous link or 'GENESIS'
    evidence_hash: Mapped[str] = mapped_column(
        String(64),
        index=True,
        nullable=False
    )  # SHA-256 of canonical payload + previous_evidence_hash

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    case: Mapped["Case"] = relationship(
        "Case",
        back_populates="evidence_items"
    )
    match: Mapped["Match"] = relationship(
        "Match",
        back_populates="evidence_item"
    )
