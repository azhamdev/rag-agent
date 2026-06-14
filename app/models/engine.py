from sqlmodel import Session, create_engine

from app.core.settings import settings

engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    connect_args={"check_same_thread": False},
)


def get_session():
    with Session(engine) as session:
        yield session
