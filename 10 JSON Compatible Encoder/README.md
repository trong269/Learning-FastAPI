# JSON Compatible Encoder
* Trong một vài  trường hợp bạn cần chuyển đổi kiểu dữ liệu (như pydantic model) sang kiểu dữ liệu tương thích với JSON ( như `dict`, `list`, etc ).

* Bạn có thể sử dụng `jsonable_encoder` để chuyển đổi dữ liệu đầu vào sang kiểu dữ liệu có thể được lưu trữ như JSON

````python
from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
````
* Trong ví dụ trên, nó đã chuyển đổi từ `pydantic model` sang `dict`, và từ `datetime` sang `str`

* Nó không trả về một `str` lớn chứa dữ liệu ở định dạng JSON (như dạng string ). Nó trả về cấu trúc dữ liệu tiêu chuẩn Python (ví dụ: `dict`) với các giá trị và giá trị phụ đều tương thích với JSON.