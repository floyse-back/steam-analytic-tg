from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.shared.config import SYNC_DATABASE_URL

engine = create_engine(url=SYNC_DATABASE_URL,echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

