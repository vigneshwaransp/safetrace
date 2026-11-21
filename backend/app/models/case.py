import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Boolean, DateTime, Uuid, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    is_pseudonymous: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    pseudonym: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="ACTIVE",
        nullable=False
    )  # ACTIVE, CLOSED, ARCHIVED
    retain_encrypted_originals: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
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
    user: Mapped["User"] = relationship(
        "User",
        back_populates="cases"
    )
    images: Mapped[List["CaseImage"]] = relationship(
        "CaseImage",
        back_populates="case",
        cascade="all, delete-orphan"
    )
    discovery_jobs: Mapped[List["DiscoveryJob"]] = relationship(
        "DiscoveryJob",
        back_populates="case",
        cascade="all, delete-orphan"
    )
    matches: Mapped[List["Match"]] = relationship(
        "Match",
        back_populates="case",
        cascade="all, delete-orphan"
    )
    evidence_items: Mapped[List["EvidenceItem"]] = relationship(
        "EvidenceItem",
        back_populates="case",
        cascade="all, delete-orphan"
    )
    reports: Mapped[List["Report"]] = relationship(
        "Report",
        back_populates="case",
        cascade="all, delete-orphan"
    )
