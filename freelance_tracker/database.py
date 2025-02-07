from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///data/freelance_tracker.db"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Bind the session
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
