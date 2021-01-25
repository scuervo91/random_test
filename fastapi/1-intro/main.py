from enum import Enum
from fastapi import FastAPI 

#predifined items
class ModelItems(str,Enum):
    santi = 910821
    juli = 960105


app = FastAPI() 


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
    
