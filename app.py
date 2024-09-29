from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    id: int
    name: str
    description: str = None
    price: float
    category: str

# menu items for demonstration purposes
items = [
    Item(id=1, name="Margherita Pizza", description="Classic pizza with tomatoes, mozzarella, and basil", price=12.99, category="pizza"),
    Item(id=2, name="Caesar Salad", description="Fresh romaine lettuce with Caesar dressing", price=8.99, category="salad"),
    Item(id=3, name="Pepperoni Pizza", description="Pizza with pepperoni slices", price=14.99, category="pizza"),
    Item(id=4, name="Spaghetti Carbonara", description="Spaghetti with creamy carbonara sauce", price=13.99, category="pasta"),
    Item(id=5, name="Garlic Bread", description="Toasted bread with garlic and butter", price=4.99, category="appetizer"),
    Item(id=6, name="Tiramisu", description="Classic Italian dessert with coffee and mascarpone", price=6.99, category="dessert"),
    Item(id=7, name="Minestrone Soup", description="Hearty vegetable soup", price=7.99, category="soup"),
    Item(id=8, name="Chicken Alfredo", description="Pasta with creamy Alfredo sauce and chicken", price=15.99, category="pasta"),
    Item(id=9, name="Greek Salad", description="Salad with feta cheese, olives, and cucumbers", price=9.99, category="salad"),
    Item(id=10, name="Bruschetta", description="Grilled bread with tomatoes and basil", price=5.99, category="appetizer"),
    Item(id=11, name="Lasagna", description="Layered pasta with meat and cheese", price=16.99, category="pasta"),
    Item(id=12, name="Chocolate Lava Cake", description="Warm chocolate cake with a molten center", price=7.99, category="dessert")
]

@app.get("/menu/", response_model=List[Item])
def get_items():
    return items

@app.get("/menu/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/menu/category/{category}", response_model=List[Item])
def get_category_items(category: str):
    category_items = [item for item in items if item.category == category]
    return category_items

@app.post("/menu/items", response_model=Item)
def create_item(item: Item):
    items.append(item)
    return item

@app.put("/menu/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            items[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.patch("/menu/items/{item_id}", response_model=Item)
def patch_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            if updated_item.name is not None:
                item.name = updated_item.name
            if updated_item.description is not None:
                item.description = updated_item.description
            if updated_item.price is not None:
                item.price = updated_item.price
            if updated_item.category is not None:
                item.category = updated_item.category
            items[index] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/menu/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            del items[index]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")