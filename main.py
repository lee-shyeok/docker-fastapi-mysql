from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os

app = FastAPI()

DB_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:secret@db:3306/mydb")
engine = create_engine(DB_URL)

@app.get("/")
def root():
    return {"message": "Hello from FastAPI + Docker!"}

@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "connected"}