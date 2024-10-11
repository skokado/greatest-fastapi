from typing import Optional
from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base

from .user import User


class UserProfile(Base):
    __tablename__ = "auth_user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[Optional[str]] = mapped_column(String(500))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255))

    user: Mapped[User] = relationship(back_populates="profile")
    user_id: Mapped[int] = mapped_column(ForeignKey(f"{User.__tablename__}.id"), unique=True, nullable=False)
