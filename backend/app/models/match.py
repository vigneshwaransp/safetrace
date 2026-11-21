import uuid
from datetime import datetime, timezone
from typing import Optional, Any
from sqlalchemy import String, DateTime, Uuid, ForeignKey, Float, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Match(Base):
    __tablename__ = "matches"

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
    discovery_job_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("discovery_jobs.id", ondelete="SET NULL"),
        index=True,
        nullable=True
    )
    case_image_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("case_images.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    platform: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )  # META, X, REDDIT, YOUTUBE, BLUESKY, WEB
    source_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )
    author_handle: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )
    post_timestamp: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    thumbnail_url: Mapped[Optional[str]] = mapped_column(
        String(1000),
        nullable=True
    )
    media_url: Mapped[Optional[str]] = mapped_column(
        String(1000),
        nullable=True
    )

    # Candidate Fingerprints
    sha256_hash: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True
    )
    pdq_hash: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True
    )
    phash: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True
    )
    dhash: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True
    )
    ahash: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True
    )

    # Scoring & Classification
    similarity_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    confidence_band: Mapped[str] = mapped_column(
        String(20),
        default="MEDIUM",
        nullable=False
    )  # HIGH, MEDIUM, LOW
    match_reasons: Mapped[Any] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )

    # Human-in-the-Loop Review
    review_status: Mapped[str] = mapped_column(
        String(50),
        default="UNREVIEWED",
        nullable=False
    )  # UNREVIEWED, CONFIRMED, REJECTED, UNSURE
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    reviewer_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    case: Mapped["Case"] = relationship(
        "Case",
        back_populates="matches"
    )
    discovery_job: Mapped[Optional["DiscoveryJob"]] = relationship(
        "DiscoveryJob",
        back_populates="matches"
    )
    case_image: Mapped["CaseImage"] = relationship(
        "CaseImage",
        back_populates="matches"
    )
    evidence_item: Mapped[Optional["EvidenceItem"]] = relationship(
        "EvidenceItem",
        back_populates="match",
        uselist=False
    )
