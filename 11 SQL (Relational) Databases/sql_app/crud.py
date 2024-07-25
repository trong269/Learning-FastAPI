from sqlalchemy.orm import Session
import models, schemas


# lấy 1 user từ user_id
def get_user( db:Session, user_id : int ):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    return db_user
# lấy 1 user từ user_email
def get_user_by_email(db:Session, user_email : str):
    return db.query(models.User).filter(models.User.email == user_email).first()
# đọc nhiều user
def get_users(db:Session, skip:int = 0, limit:int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
#lấy một item
def get_item(db:Session, item_id: int ):
    return db.query(models.Item).filter(models.Item.id == item_id).first()
# lấy nhiều item
def get_items(db:Session, skip:int = 0 , limit:int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()
# tạo một user mới
def create_user(db:Session, user:schemas.UserCreate):
    hashed_password = user.password + "hashed_password" # chỉ mang tính chất minh họa, trong thực tế cần sử dụng thuật toán để hashing password
    db_user = models.User(email = user.email, hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
# Tạo mới một item và liên kết nó với một người dùng cụ thể
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# cập nhật user
def update_user_email(db: Session, user_id: int, user_update: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.email = user_update.email
        # Không cập nhật password trong ví dụ này, nhưng bạn có thể thêm vào nếu cần
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user
# cập nhật item
def update_item(db: Session, item_id: int, item_update: schemas.ItemBase):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db_item.title = item_update.title
        db_item.description = item_update.description
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    return db_item
# Xóa user
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
# Xóa item
def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

