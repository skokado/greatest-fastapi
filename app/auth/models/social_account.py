from typing import Optional
from uuid import UUID

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base

from .user import User


class SocialAccount(Base):
    __tablename__ = "auth_social_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str] = mapped_column(String(20), nullable=False)
    social_id: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255))

    user: Mapped[User] = relationship(back_populates="social_accounts")
    user_id: Mapped[int] = mapped_column(ForeignKey(f"{User.__tablename__}.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("provider", "social_id", name="uq_provider_social_id"),
    )
