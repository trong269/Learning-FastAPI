from sqlalchemy.orm import Session
from . import models, schemas
# lấy 1 user từ user_id
def get_user( db:Session, user_id : int ):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    return db_user
# lấy 1 user từ user_email
def get_user_by_email(db:Session, user_email : str):
    return db.query(models.User).filter(models.User.email == user_email)
# đọc nhiều user
def get_users(db:Session, skip:int = 0, limit:int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
# lấy nhiều item
def get_items(db:Session, skip:int = 0 , limit:int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()
# tạo một user mới
def create_user(db:Session, user:schemas.UserCreate):
    hashed_password = user.password + "hashed_password" # chỉ mang tính chất minh họa, trong thực tế cần sử dụng thuật toán để hashing password
    db_user = models.User(email = user.email, hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh()
    return db_user
# Tạo mới một item và liên kết nó với một người dùng cụ thể
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item