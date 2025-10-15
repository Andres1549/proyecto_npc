from sqlmodel import create_engine, Session
from sqlmodel import SQLModel
from typing import Generator

sqlite_file_name = "../npcs.db"
sqlite_url = "sqlite:///npcs.db"


engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
