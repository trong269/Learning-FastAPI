# SQL (Relational) Databases

Bạn có thể sử dụng bất kỳ relational database nào bạn muốn
## ORMs (object-relational mapping)
* ORM có công cụ chuyển đổi ("map") giữa object trong code và database table ("relation")
* với ORM, bạn có thể dễ dàng tạo ra một **class** nó đại diện cho một **table** trong SQL database, mỗi **attribute** của class đậi diện cho một **column** của table
* mỗi **instance object** của class đại diện cho một **row** của table

Một vài ORMs phổ biến: Django-ORM, SQLAlchemy, Peewee, ...

Ở đây, chúng ta sẽ sử dụng: **SQLAlchemy**

### File structure
giả sử bạn đang có thư mục `my_super_project` nó chứa một thư mục con là `sql_app` với cấu trúc như sau:

```
.
└── sql_app
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    ├── models.py
    └── schemas.py
```
Với file `__init__.py` là một file rỗng, nhưng nó sẽ cho Python biết `sql_app` với tất cả các modules của nó là một `package`

### 0. Đầu tiên cần install SQLAlchemy và MySQL Driver
```
pip install sqlalchemy pymysql
```
### 1. Kết nối với cơ sở dữ liệu
Hãy truy cập vào `sql_app/database.py`

```python
# import thư viện
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
'''
create_engine: Hàm này từ SQLAlchemy được sử dụng để thiết lập kết nối với cơ sở dữ liệu
declarative_base: Hàm này tạo ra một lớp cơ sở mà tất cả các models ORM của bạn sẽ kế thừa. Nó là phần cơ bản của mô hình đối tượng quan hệ (ORM).
sessionmaker: Hàm này tạo ra một lớp Session mà bạn sẽ sử dụng để tương tác với cơ sở dữ liệu.
'''
# cấu hình kết nối CSDL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"
# tạo engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# tạo SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# tạo base
Base = declarative_base()
```
Đoạn mã này thiết lập cấu hình kết nối đến cơ sở dữ liệu và chuẩn bị các thành phần cơ bản của SQLAlchemy như `engine`, `sessionmaker`, và `Base`. Đây là các bước quan trọng để chuẩn bị môi trường tương tác với cơ sở dữ liệu trong ứng dụng FastAPI của bạn.

### 2. Tạo Database Models
Chúng ta sẽ sử dụng `Base` class trước đó để tạo SQLAlchemy models.
Những Class này là SQLAlchemy models:
```python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)
    items = relationship('Item', back_populates='owner')

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), index=True)
    description = Column(String(255))
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='items')
```
* Thuộc tính `__tablename__` cho SQLAlchemy biêt tên của mỗi table sử dụng trong CSDL cho từng model này

* Tạo model attributes (columns). Ta sử dụng `Column` từ SQLAlchemy 
* Tạo Relationship, Ta sử dụng `relationship` được cung cấp bởi `sqlalchemy.orm`
    * khi truy cập vào thuộc tính `items` trong `User`, nó sẻ chứa một danh sách `Item` SQLAlchemy models (từ `items table`) có Foreign key chỉ tới record này trong `users table`
    * khi truy cập vào thuộc tính `owner` trong `Item`, nó sẽ chứa `User` SQLAlchemy model (từ `users table`). Nó sẽ sử dụng `owner_id` (foreign key) để biết record nào để lấy từ `user table` 

### 3. tạo Pydantic model(schemas)
Tạo pydantic model(schemas) sẽ được sử dụng khi đọc dữ liệu và khi trả về dữ liệu từ API

Những models này giúp đảm bảo rằng dữ liệu đầu vào và đầu ra của các endpoint trong ứng dụng FastAPI được kiểm tra và hợp lệ
```python
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str
class ItemCreate(ItemBase):
    pass
class Item(ItemBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True
# lớp dùng chung cho các thuộc tính cơ bản của user
class  UserBase(BaseModel):
    email:str
# lớp dùng để  tạo mới user
class UserCreate(UserBase):
    password:str
# lớp đại diện cho user đầy đủ 
class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []
    class Config:
        orm_mode = True
```
* `Config` class được dùng để cung cấp configuration đến pydantic
*  Khi `orm_mode` được đặt thành `True` trong cấu hình của một Pydantic model, nó cho phép model đó chấp nhận các đối tượng ORM trực tiếp như đầu vào để tạo ra các phiên bản của chính nó.

### 4. CRUD utils
#### Read
```python
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
```
#### Create
Tạo một SQLAlchemy model instance với dữ liệu của bạn
* `add()`: thêm instance object vào phiên làm việc
* `commit()`: lưu các đối tượng trong phiên làm việc vào CSDL
* `refresh()`: làm mới, đảm bảo rằng đối tượng đã được thêm vào trong CSDL

```python
from sqlalchemy.orm import Session
from . import models, schemas

# tạo một user mới
def create_user(db:Session, user:schemas.UserCreate):
  # hashed_password chỉ mang tính chất minh họa, trong thực tế cần sử dụng thuật toán để hashing password
    hashed_password = user.password + "hashed_password" 
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
```
