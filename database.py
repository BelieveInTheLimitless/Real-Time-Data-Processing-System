from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_CONFIG
from models import Base
import time

DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    retries = 5
    for i in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("Database initialized successfully.")
            break
        except Exception as e:
            print(f"Database connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
    else:
        raise Exception("Could not connect to the database after retries.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
