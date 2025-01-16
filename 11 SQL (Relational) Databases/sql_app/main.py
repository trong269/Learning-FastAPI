from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import crud, schemas, models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User, tags= ['User'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User], tags= ['User'])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags= ['User'])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item, tags=['Item'])
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User does not exist')
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item], tags=['Item'])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.put('/users/{user_id}', response_model=schemas.User, tags= ['User'])
async def update_user_email(user_id : int , user_update: schemas.UserCreate, db: Session= Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User does not exist')
    return crud.update_user_email(db=db, user_id=user_id, user_update=user_update )

@app.put('/items/{item_id}', response_model=schemas.Item, tags=['Item'])
async def update_item( item_id : int , item_update: schemas.ItemBase, db:Session = Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail='Item does not exist')
    return crud.update_item(db=db, item_id=item_id, item_update=item_update)

@app.delete('/users/{user_id}', response_model=schemas.User, tags= ['User'])
async def delete_user(user_id : int , db:Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User does not exist')
    return crud.delete_user(user_id=user_id, db=db)

@app.delete('/items/{item_id}', response_model=schemas.Item, tags=['Item'])
async def delete_item(item_id : int , db:Session= Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail='Item does not exist')
    return crud.delete_item(item_id=item_id, db=db)
