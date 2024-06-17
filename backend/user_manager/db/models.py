from datetime import datetime

from config import settings
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column, ForeignKey, Integer, MetaData, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

metadata_obj = MetaData(schema=settings.DB_SCHEMA)






Base = declarative_base(metadata=metadata_obj)

repr_cols_num = 12


def __repr__(self):
    cols = []
    for idx, col in enumerate(self.__table__.columns.keys()):
        if idx < repr_cols_num:
            cols.append(f"{col}={getattr(self, col)}")
    return f"<{self.__class__.__name__}({cols})>"


Base.__repr__ = __repr__


class Task(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    target_date: Mapped[datetime] = mapped_column(nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    users: Mapped[list["TaskUser"]] = relationship(back_populates="task")


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    id: int = Column(Integer, primary_key=True, nullable=False)
    email: str = Column(String(length=320), unique=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    role: str = Column(String(length=100), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    tasks: Mapped[list["TaskUser"]] = relationship(back_populates="user")


class TaskUser(Base):
    __tablename__ = "task_user"
    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    task: Mapped["Task"] = relationship(back_populates="users")
    user: Mapped["User"] = relationship(back_populates="tasks")
