import atexit
import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import DateTime, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

load_dotenv()

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(PG_DSN)  # создание подключения
Session = sessionmaker(bind=engine)  # фабрика для создания сессий

# регистрируем функции, которые должны будут выполниться после завершения работы нашего приложения
# чтобы не создавать лишние подключения к БД и тд
atexit.register(engine.dispose)  # закрываем подключение к БД


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""

    pass


class User(Base):
    __tablename__ = "app_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    registration_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()  # база сама запишет дату и время
    )

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registration_time": self.registration_time.isoformat(),
        }


Base.metadata.create_all(bind=engine)
