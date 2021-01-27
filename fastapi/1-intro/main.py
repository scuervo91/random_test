from enum import Enum
from fastapi import FastAPI, Query, Path
from typing import Optional
from pydantic import BaseModel
#predifined items
class ModelItems(str,Enum):
    santi = 910821
    juli = 960105


app = FastAPI() 

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class  Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float 
    tax: Optional[float] = None
    

@app.get("/items/mine")
async def read_item_mine():
    return {"item_id":"Mee"}

@app.get("/items/{item_id}")
async def read_item(item_id:int):
    return {"item_id":item_id}

@app.get("/models/{model_id}")
async def read_model(model_id: ModelItems):
    if model_id == ModelItems.santi:
        return {"model_id": model_id, "message": "Santi Model"}
    else:
        return {"model_id": model_id, "message": "Juli Model"}
    
@app.get("/db/")
async def read_db(skip: int, limit: int):
    return fake_items_db[skip : skip + limit]

@app.get("/optional/{item_id}")
async def read_optional(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


## Pydantic POST Request

@app.post("/items/{item_id}")
async def create_item(item: Item, item_id: int):
    return {'item_id':item_id,**item.dict()}

@app.get("/crows/")
async def get_crow(crow : str = Query(...,min_length=2, max_length=5)):
    return {'crow':crow}

@app.get("/crows/{crow_id}")
async def get_crow(crow_id : int = Path(...,ge=3),crow : str = Query(...,min_length=2, max_length=5)):
    return {'crow_id':crow_id,'crow':crow}