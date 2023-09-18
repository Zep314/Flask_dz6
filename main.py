import sqlalchemy
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import model as md
import view
from typing import List


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

engine = sqlalchemy.create_engine(md.DATABASE_URL)
md.metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    await md.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await md.database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/users/")
async def create_user(user: md.UserIn):
    return await view.create_user(user)


@app.put("/users/{user_id}")
async def update_user(user_id: int, new_user: md.UserIn):
    return await view.update_user(user_id, new_user)


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    return await view.delete_user(user_id)


@app.get("/users/", response_model=List[md.User])
async def read_users():
    return await view.read_users()


@app.post("/products/")
async def create_user(product: md.ProductIn):
    return await view.create_product(product)


@app.put("/products/{product_id}")
async def update_user(product_id: int, new_product: md.ProductIn):
    return await view.update_product(product_id, new_product)


@app.delete("/products/{product_id}")
async def delete_user(product_id: int):
    return await view.delete_product(product_id)


@app.get("/products/", response_model=List[md.Product])
async def read_users():
    return await view.read_products()


@app.post("/orders/")
async def create_order(order: md.OrderIn):
    return await view.create_order(order)


@app.put("/orders/{order_id}")
async def update_user(order_id: int, new_order: md.OrderIn):
    return await view.update_order(order_id, new_order)


@app.delete("/orders/{order_id}")
async def delete_user(order_id: int):
    return await view.delete_order(order_id)


@app.get("/orders/", response_model=List[md.Order])
async def read_users():
    return await view.read_orders()


# Запуск:
# uvicorn main:app --reload

# curl -H "accept: application/json" -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/users/ -d "{\"first_name\": \"Ivan\", \"last_name\": \"Ivanov\", \"email\": \"ivan@mail.ru\", \"password\": \"SuperPa$$w0rd\"}"
# curl -H "accept: application/json" -H "Content-Type: application/json" -X PUT http://127.0.0.1:8000/users/2 -d "{\"first_name\": \"Mike\", \"last_name\": \"Jacson\", \"email\": \"mike@nasa.com\", \"password\": \"IWantToBeleve\"}"
# curl -H "accept: application/json" -X DELETE http://127.0.0.1:8000/users/2
# curl -H "accept: application/json" -X GET http://127.0.0.1:8000/users/

# curl -H "accept: application/json" -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/products/ -d "{\"name\": \"cookies\", \"description\": \"Grand cookies\", \"cost\": 3.5}"
# curl -H "accept: application/json" -H "Content-Type: application/json" -X PUT http://127.0.0.1:8000/products/2 -d "{\"name\": \"kakes\", \"description\": \"Multicake\", \"cost\": 25.3}"
# curl -H "accept: application/json" -X DELETE http://127.0.0.1:8000/products/3
# curl -H "accept: application/json" -X GET http://127.0.0.1:8000/products/

# curl -H "accept: application/json" -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/orders/ -d "{\"user_id\": 1, \"product_id\": 1, \"order_date\": \"2023-09-10 10:00:00.0\", \"order_status\": \"processing\"}"
# curl -H "accept: application/json" -H "Content-Type: application/json" -X PUT http://127.0.0.1:8000/orders/1 -d "{\"user_id\": 2, \"product_id\": 2, \"order_date\": \"2023-09-11 11:11:11.1\", \"order_status\": \"complete\"}"
# curl -H "accept: application/json" -X DELETE http://127.0.0.1:8000/orders/2
# curl -H "accept: application/json" -X GET http://127.0.0.1:8000/orders/
