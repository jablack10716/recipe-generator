from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./recipes.db"

# SQLite needs check_same_thread when used with FastAPI's threadpool
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()

def get_db():
    """Provide a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
