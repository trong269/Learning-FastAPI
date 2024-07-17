from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

db = [Item( name = 'Smart Phone', price= 100.0 , tax = 1.0 ,)]

app = FastAPI()

@app.post('/item/', response_model=Item)
async def add_item(item : Item ):
    db.append(item)
    return item

@app.get('/item/', response_model= list[Item])
async def get_item():
    return [
        Item(name = 'Smart Phone', price= 10000),
        Item(name = 'snack', price= 200)
    ]
