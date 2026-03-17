from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UserProgress(Base):
    __tablename__ = "user_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    learner_name: Mapped[str] = mapped_column(String(100), nullable=False)
    cefr_level: Mapped[str] = mapped_column(String(10), nullable=False, default="A1")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
