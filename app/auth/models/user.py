from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from config.db import Base


if TYPE_CHECKING:
    from .user_profile import UserProfile
    from .social_account import SocialAccount


class User(Base):
    __tablename__ = "auth_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Fields for social OAuth
    oauth_provider: Mapped[Optional[str]] = mapped_column(String(20))
    oauth_sub: Mapped[Optional[str]] = mapped_column(String(255))
    oauth_access_token: Mapped[Optional[str]] = mapped_column(String(255))
    oauth_refresh_token: Mapped[Optional[str]] = mapped_column(String(255))
    oauth_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    profile: Mapped["UserProfile"] = relationship(back_populates="user", uselist=False)
    social_accounts: Mapped[list["SocialAccount"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email
