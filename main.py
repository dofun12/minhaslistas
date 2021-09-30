# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from mongodb_service import MongoDBService
from typing import Optional
from fastapi import FastAPI, Response
from fastapi import FastAPI
from pprint import pprint
import json
import uvicorn
from bson import json_util

app = FastAPI()


@app.get("/")
def read_root():
    mongodb = MongoDBService()
    list = mongodb.list()
    print(list)
    return Response(content=json.dumps(list, default=json_util.default), media_type="application/json")


@app.get("/lista/{list_name}")
def read_item(list_name: str, q: Optional[str] = None):
    mongodb = MongoDBService()
    lista = json.dumps(mongodb.list_by_name(list_name))
    print(lista)
    return Response(content=lista, media_type="application/json")


@app.put("/lista/{list_name}")
def put_item(list_name: str, q: Optional[str] = None):
    mongodb = MongoDBService()
    try:
        data = mongodb.list_by_name(list_name)
        return {"success": True, "message": list_name + " Created!", "data": data}
    except Exception as e:
        return {"success": False, "error": e}




@app.get("/items/{item_id}")
def other_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    mongodb = MongoDBService()
    list_name = "outra"
    mongodb.create_list(list_name)
    mongodb.add_list_item(list_name, "itemA")
    for item in mongodb.list():
        print(item)
    print("Adicionando...")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
