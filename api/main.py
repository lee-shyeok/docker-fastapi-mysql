from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Day 2 - MySQL connected!'}

@app.post('/items')
def create_item(name: str, description: str = '', db: Session = Depends(get_db)):
    item = models.Item(name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get('/items')
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()
