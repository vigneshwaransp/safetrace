import uuid
from datetime import datetime, timezone
from typing import List, Optional, Any
from sqlalchemy import String, DateTime, Uuid, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class DiscoveryJob(Base):
    __tablename__ = "discovery_jobs"

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
    status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING",
        nullable=False
    )  # PENDING, RUNNING, COMPLETED, FAILED
    platforms_searched: Mapped[Any] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )
    results_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
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
        back_populates="discovery_jobs"
    )
    matches: Mapped[List["Match"]] = relationship(
        "Match",
        back_populates="discovery_job"
    )
