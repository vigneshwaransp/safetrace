import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,
    TokenRefresh,
)
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.api.deps import get_current_user, record_audit

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserRegister,
    request: Request,
    db: Session = Depends(get_db)
):
    """Register a new user account with Argon2 password hashing."""
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role.upper() if user_in.role.upper() in ["USER", "NGO", "ADMIN"] else "USER",
        is_active=True,
        is_verified=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    record_audit(
        db=db,
        action="USER_REGISTERED",
        user_id=user.id,
        details={"email": user.email, "role": user.role},
        request=request
    )

    return user


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """Authenticate with email and password, issuing access & refresh tokens."""
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is inactive"
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    record_audit(
        db=db,
        action="USER_LOGIN_SUCCESS",
        user_id=user.id,
        details={"email": user.email},
        request=request
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=3600,
        user=UserResponse.model_validate(user),
    )


@router.post("/refresh")
def refresh_token(
    refresh_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """Exchange a valid refresh token for a new access token."""
    try:
        payload = decode_token(refresh_data.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing token subject"
            )
        user_id = uuid.UUID(user_id_str)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token: {str(e)}"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    new_access_token = create_access_token(user.id)
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": 3600,
    }


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    """Retrieve profile of currently authenticated user."""
    return current_user
