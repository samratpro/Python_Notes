### Install library
```bash
pip install "fastapi[all]"
```
### Run Server
```bash
uvicorn file_name:app --reload
```
### Load Server
```bash
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/openapi.json
http://127.0.0.1:8000/redoc
```
### Initial Code
```py
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}
```
### fastAdmin
```
https://vsdudakov.github.io/fastadmin/
```
### Pass Data with Path Parameter
```py
@app.get("/path/{data}")
async def root(data):
    # root(data:int)
    return {"data": data}
    # return ['data1','data2']
# http://127.0.0.1:8000/items/data
```

### Query Parameter
```py
fake_list = [{"item": "Samrat"}, {"item": "Bar"}, {"item": "Baz"}]
@app.get("/items/")
async def read_item(start: int = 0, end: int=3):
    return fake_list[start:end]
# http://127.0.0.1:8000/items/?start=0&end=3
```
### Query + Path Parameter with logic
```py
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
# http://127.0.0.1:8000/items/2?q=3
```
### Request Body With Post Method
```py
from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### Request body + path parameters
```py
class Item(BaseModel):
    pass

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}
```
### Request body + path + query parameters
```py
class Item(BaseModel):
    pass
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
```
### Request Body With Image
```py
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
app = FastAPI()
class Image(BaseModel):
    url: HttpUrl
    name: str
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```
### Read Cookie
```py
from fastapi import Cookie
@app.get("/read_cookie/")
async def read_cookie(cookie_token: str = Cookie(None)):
    return {"cookie_token": cookie_token}
```
### Read User Agent
```py
from fastapi import Request
@app.get("/user-agent/")
async def get_user_agent(request: Request):
    user_agent = request.headers.get("User-Agent")
    return {"user_agent": user_agent}
```
