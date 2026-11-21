import uuid
from datetime import datetime, timezone
from typing import Optional, Any
from sqlalchemy import String, DateTime, Uuid, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
        nullable=True
    )
    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("cases.id", ondelete="SET NULL"),
        index=True,
        nullable=True
    )
    action: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False
    )
    ip_address: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )
    user_agent: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )
    details: Mapped[Any] = mapped_column(
        JSON,
        default=dict,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="audit_logs"
    )
