import atexit
from datetime import datetime

from sqlalchemy import DateTime, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


PG_DSN = f"postgresql://app:secret@127.0.0.1:5431/netology"

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)
atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class Advertisement(Base):
    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[str] = mapped_column(String(40), nullable=False, index=True)

    @property
    def dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "owner": self.owner,
        }


Base.metadata.create_all(bind=engine)
