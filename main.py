import sqlalchemy
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import model as md
import view
from typing import List, Annotated
from fastapi.responses import HTMLResponse, RedirectResponse
import starlette.status as status
from model.my_logger import logger

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
    return RedirectResponse("/web/users")


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
async def create_product(product: md.ProductIn):
    return await view.create_product(product)


@app.put("/products/{product_id}")
async def update_product(product_id: int, new_product: md.ProductIn):
    return await view.update_product(product_id, new_product)


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    return await view.delete_product(product_id)


@app.get("/products/", response_model=List[md.Product])
async def read_products():
    return await view.read_products()


@app.post("/orders/")
async def create_order(order: md.OrderIn):
    return await view.create_order(order)


@app.put("/orders/{order_id}")
async def update_order(order_id: int, new_order: md.OrderIn):
    return await view.update_order(order_id, new_order)


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    return await view.delete_order(order_id)


@app.get("/orders/", response_model=List[md.Order])
async def read_orders():
    return await view.read_orders()


@app.get("/web/users", response_class=HTMLResponse)
async def web_read_users(request: Request):
    all_users = await read_users()
    return templates.TemplateResponse("users.html", {"request": request, "users": all_users})


@app.post("/web/users", response_class=HTMLResponse)
async def web_create_user(first_name: Annotated[str, Form()],
                          last_name: Annotated[str, Form()],
                          email: Annotated[str, Form()],
                          password: Annotated[str, Form()]
                          ):
    await create_user(md.UserIn(first_name=first_name,
                                last_name=last_name,
                                email=email,
                                password=password,
                                ))
    return RedirectResponse("/web/users", status_code=status.HTTP_302_FOUND)  # Конвертируем post запрос в get


@app.post("/web/user/show_update")
async def web_show_update_user(user_id: Annotated[int, Form()], request: Request):
    all_users = await read_users()
    for user1 in all_users:
        if user1['id'] == user_id:
            break
    user = {'id': user1.id, 'first_name': user1.first_name, 'last_name': user1.last_name, 'email': user1.email,
            'password': user1.password, 'created_at': user1.created_at}
    return templates.TemplateResponse("user.html", {"request": request, "user": user})


@app.post("/web/user/update")
async def web_update_user(id: Annotated[int, Form()],
                          first_name: Annotated[str, Form()],
                          last_name: Annotated[str, Form()],
                          email: Annotated[str, Form()],
                          password: Annotated[str, Form()],
                          created_at: Annotated[str, Form()],
                          ):
    await update_user(id, md.UserIn(first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    password=password
                                    ))
    return RedirectResponse("/web/users", status_code=status.HTTP_302_FOUND)  # Конвертируем post запрос в get


@app.post("/web/user/delete")
async def web_delete_user(user_id: Annotated[int, Form()]):
    await delete_user(user_id)
    return RedirectResponse("/web/users", status_code=status.HTTP_302_FOUND)  # Конвертируем post запрос в get


@app.get("/web/user", response_class=HTMLResponse)
async def web_create_user(request: Request):
    user = {'id': 0, 'first_name': '', 'last_name': '', 'email': '', 'password': '', 'created_at': ''}
    return templates.TemplateResponse("user.html", {"request": request, "user": user})


# ================================


@app.get("/web/products", response_class=HTMLResponse)
async def web_read_products(request: Request):
    all_products = await read_products()
    return templates.TemplateResponse("products.html", {"request": request, "products": all_products})


@app.post("/web/products", response_class=HTMLResponse)
async def web_create_product(name: Annotated[str, Form()],
                             description: Annotated[str, Form()],
                             cost: Annotated[float, Form()],
                             ):
    await create_product(md.ProductIn(name=name,
                                      description=description,
                                      cost=float(cost),
                                      ))
    return RedirectResponse("/web/products", status_code=status.HTTP_302_FOUND)  # Конвертируем post запрос в get


@app.post("/web/product/show_update")
async def web_show_update_product(product_id: Annotated[int, Form()], request: Request):
    all_products = await read_products()
    for product1 in all_products:
        if product1['id'] == product_id:
            break
    product = {'id': product1.id, 'name': product1.name, 'description': product1.description,
               'cost': str(product1.cost), 'created_at': product1.created_at}
    return templates.TemplateResponse("product.html", {"request": request, "product": product})


@app.post("/web/product/update")
async def web_update_product(id: Annotated[int, Form()],
                             name: Annotated[str, Form()],
                             description: Annotated[str, Form()],
                             cost: Annotated[float, Form()],
                             created_at: Annotated[str, Form()],
                             ):
    await update_product(id, md.ProductIn(name=name,
                                          description=description,
                                          cost=float(cost),
                                          ))
    return RedirectResponse("/web/products", status_code=status.HTTP_302_FOUND)  # Конвертируем post запрос в get


@app.post("/web/product/delete")
async def web_delete_product(product_id: Annotated[int, Form()]):
    await delete_product(product_id)
    return RedirectResponse("/web/products", status_code=status.HTTP_302_FOUND)  # Конвертируем post запрос в get


@app.get("/web/product", response_class=HTMLResponse)
async def web_create_product(request: Request):
    product = {'id': 0, 'name': '', 'description': '', 'cost': '', 'created_at': ''}
    return templates.TemplateResponse("product.html", {"request": request, "product": product})


@app.get("/web/orders", response_class=HTMLResponse)
async def web_read_orders(request: Request):
    all_orders = await read_orders()
    return templates.TemplateResponse("orders.html", {"request": request, "orders": all_orders})


@app.post("/web/orders", response_class=HTMLResponse)
async def web_create_order(user_id: Annotated[int, Form()],
                           product_id: Annotated[int, Form()],
                           order_date: Annotated[str, Form()],
                           order_status: Annotated[str, Form()],
                           ):
    await create_order(md.OrderIn(user_id=int(user_id),
                                  product_id=int(product_id),
                                  order_date=order_date,
                                  order_status=order_status,
                                  ))
    return RedirectResponse("/web/orders", status_code=status.HTTP_302_FOUND)  # Конвертируем post запрос в get


@app.post("/web/order/show_update")
async def web_show_update_order(order_id: Annotated[int, Form()], request: Request):
    all_orders = await read_orders()
    for order1 in all_orders:
        if order1['id'] == order_id:
            break
    order = {'id': order1.id, 'user_id': order1.user_id, 'product_id': order1.product_id,
             'order_date': order1.order_date, 'order_status': order1.order_status, 'created_at': order1.created_at}
    return templates.TemplateResponse("order.html", {"request": request, "order": order})


@app.post("/web/order/update")
async def web_update_order(id: Annotated[int, Form()],
                           user_id: Annotated[int, Form()],
                           product_id: Annotated[int, Form()],
                           order_date: Annotated[str, Form()],
                           order_status: Annotated[str, Form()],
                           created_at: Annotated[str, Form()],
                           ):
    await update_order(id, md.OrderIn(user_id=int(user_id),
                                      product_id=int(product_id),
                                      order_date=order_date,
                                      order_status=order_status,
                                      ))
    return RedirectResponse("/web/orders", status_code=status.HTTP_302_FOUND)  # Конвертируем post запрос в get


@app.post("/web/order/delete")
async def web_delete_order(order_id: Annotated[int, Form()]):
    await delete_order(order_id)
    return RedirectResponse("/web/orders", status_code=status.HTTP_302_FOUND)  # Конвертируем post запрос в get


@app.get("/web/order", response_class=HTMLResponse)
async def web_create_order(request: Request):
    order = {'id': 0, 'user_id': 0, 'product_id': 0, 'order_date': '', 'order_status': '', 'created_at': ''}
    return templates.TemplateResponse("order.html", {"request": request, "order": order})

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
