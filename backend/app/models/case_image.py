import uuid
from datetime import datetime, timezone
from typing import List, Optional, Any
from sqlalchemy import String, Boolean, DateTime, Uuid, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class CaseImage(Base):
    __tablename__ = "case_images"

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
    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    storage_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )
    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    
    # Image Fingerprints (Perceptual & Exact)
    sha256_hash: Mapped[str] = mapped_column(
        String(64),
        index=True,
        nullable=False
    )
    pdq_hash: Mapped[Optional[str]] = mapped_column(
        String(64),
        index=True,
        nullable=True
    )
    pdq_quality: Mapped[Optional[int]] = mapped_column(
        Integer,
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
    keypoints_summary: Mapped[Optional[Any]] = mapped_column(
        JSON,
        nullable=True
    )
    
    # Privacy / Zero-Knowledge Flags
    is_encrypted: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    is_original_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    case: Mapped["Case"] = relationship(
        "Case",
        back_populates="images"
    )
    matches: Mapped[List["Match"]] = relationship(
        "Match",
        back_populates="case_image",
        cascade="all, delete-orphan"
    )
