from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Mock database
db = []

# Pydantic model for the item
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# CRUD operations
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    db.append(item)
    return item

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    try:
        return db[item_id - 1]
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    try:
        db[item_id - 1] = item
        return item
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    try:
        item = db.pop(item_id - 1)
        return {"message": f"Deleted item: {item.name}"}
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")
