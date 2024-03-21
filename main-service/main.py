from fastapi import FastAPI, Depends, Request, Form, status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from schemas import Products
from database import SessionLocal, engine

import models
import uvicorn

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
        print("this is working")
    finally:
        db.close()

@app.get("/")
async def home(req: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return {"message":"hello world"}

# @app.get("/test")
# async def root():
#     return {"message":"hello world"}

@app.post("/product")
def create(product: Products,db: Session = Depends(get_db)):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


if __name__ == "__main__":
 uvicorn.run("main:app", host="0.0.0.0", port=8080,reload=True)  