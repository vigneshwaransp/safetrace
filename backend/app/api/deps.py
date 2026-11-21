import uuid
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise credentials_exception
        user_id_str: str = payload.get("sub")
        if not user_id_str:
            raise credentials_exception
        user_id = uuid.UUID(user_id_str)
    except Exception:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user account")
    return user


def get_current_active_ngo_or_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role not in ["NGO", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have sufficient privileges"
        )
    return current_user


def record_audit(
    db: Session,
    action: str,
    user_id: Optional[uuid.UUID] = None,
    case_id: Optional[uuid.UUID] = None,
    details: Optional[Dict[str, Any]] = None,
    request: Optional[Request] = None,
) -> AuditLog:
    """Helper to record audit trail entries."""
    ip_address = request.client.host if request and request.client else None
    user_agent = request.headers.get("user-agent") if request else None

    audit_entry = AuditLog(
        user_id=user_id,
        case_id=case_id,
        action=action,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details or {},
    )
    db.add(audit_entry)
    db.commit()
    db.refresh(audit_entry)
    return audit_entry
