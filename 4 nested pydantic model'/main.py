from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
class Image(BaseModel):
    url: str
    name: str
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    image: Image | None = None


db = [Item( name = 'Smart Phone', price= 100.0 , tax = 1.0 , image = Image( url="https:", name="Smart Phone"))]

app = FastAPI()

@app.post('/item/')
async def add_item(item : Item ):
    db.append(item)
    return item

@app.get('/item/{item_name}/')
async def get_item( item_name : str ):
    for i in db:
        if i.name == item_name:
            return i
    raise HTTPException(status_code= 404, detail='Item not found')
