from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from external_functions import send_telegram_message
import datetime
import pytz
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from fastapi.staticfiles import StaticFiles
from bot_instance import dp, bot_storage_key, server_cart
from postgress_functions import insert_order, insert_total_summ
from pathlib import Path
from fastapi.responses import HTMLResponse

f_api = FastAPI(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
)

templ_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=templ_dir)

static_dir = Path(__file__).parent / "static"
f_api.mount("/static", StaticFiles(directory=static_dir), name="static")

pizzas = [
    {"id": 1, "name": "Margorita", "image": "margherita.png", "description": "Томатный соус, моцарелла, базилик.", 'price': 15},
    {"id": 2, "name": "Pepperoni", "image": "pepperoni.png", "description": "Томатный соус, моцарелла, пепперони.", 'price': 16},
    {"id": 3, "name": "Four Cheese", "image": "four_cheese.png", "description": "Моцарелла, пармезан, горгонзола, эмменталь.", 'price': 17},
    {"id": 4, "name": "Hawaii", "image": "hawaiian.png", "description": "Томатный соус, моцарелла, ананасы, ветчина.", 'price': 18}
]

@f_api.post("/receive_telegram_data")
async def receive_telegram_data(data: dict):
    print("📦 Полученные данные от Telegram:", data)
    return {"success": True, "received_data": data}

@f_api.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "pizzas": pizzas})

@f_api.get("/pizza/{pizza_id}")
async def pizza_detail(request: Request, pizza_id: int):
    pizza = next((p for p in pizzas if p["id"] == pizza_id), None)
    if not pizza:
        raise HTTPException(status_code=404, detail="Пицца не найдена")
    return templates.TemplateResponse("pizza.html", {"request": request, "pizza": pizza})

@f_api.post("/cart")
async def cart_page(data: dict):
    user_name = data.get('name')
    user_id = int(data.get('user_id'))
    address = data.get("address")
    phone = data.get("phone")
    payment = data.get("payment")
    order = data.get("order", [])

    if not address or not phone:
        raise HTTPException(status_code=400, detail="Заполните все поля!")

    message = (f"🛒 *Заказ оформлен!*\n"
               f"👤 *Заказчик:* {user_name}\n"
               f"📍 *Адрес:* {address}\n"
               f"📞 *Телефон:* {phone}\n"
               f"💳 *Оплата:* {payment}\n"
               f"🍕 *Состав заказа:*\n")
    total_price = sum(item.get("price", 0) * item.get("quantity", 1) for item in order)
    order_user = f'{user_name}, {phone}'

    for item in order:
        order_line = f"• {item['name']} x{item['quantity']} - {item['price'] * item['quantity']} €\n"
        message += order_line
        order_user += order_line
    message += f"\n💰 *Сумма к оплате:* {total_price} €"

    send_telegram_message(message, user_id)  # Посылаю сообщение в телеграм

    berlin_tz = pytz.timezone("Europe/Berlin")
    formatted_time = datetime.datetime.now(berlin_tz).replace(second=0, microsecond=0).strftime("%H:%M %d.%m.%Y")
    order_user += f' Total {total_price} Data : {formatted_time}'

    bot_dict = await dp.storage.get_data(key=bot_storage_key)
    us_dict = bot_dict.get(str(user_id), {})
    us_index = len(us_dict.setdefault('order', {})) + 1
    us_dict['order'][us_index] = order_user
    await dp.storage.update_data(key=bot_storage_key, data=bot_dict)

    await insert_order(user_id)
    await insert_total_summ(user_id, total_price)

    temp = server_cart.setdefault(user_id, [])
    temp.clear()  # сбрасываю козину

    return {"success": True}

@f_api.post("/add-to-cart")
async def add_to_cart(data: dict):
    # print("\n\n\nКлючи server_cart:\n\n", server_cart.keys())
    pizza_id = data.get("pizza_id")
    quantity = data.get("quantity")
    pizza_price = data.get("price")
    user_id = int(data.get("user_id"))

    pizza = next((p for p in pizzas if p["id"] == int(pizza_id)), None)
    if not pizza:
        raise HTTPException(status_code=404, detail="Пицца не найдена")

    server_cart.setdefault(user_id, [])  # Если корзина упала - создаю ее принудительно и записываю туда id

    existing_pizza = next((item for item in server_cart[user_id] if item["pizza_id"] == pizza_id), None)
    if existing_pizza:
        existing_pizza["quantity"] += quantity
    else:
        server_cart[user_id].append(
            {"pizza_id": pizza_id, "name": pizza["name"], "quantity": quantity, 'price': pizza_price * quantity})

    return {"success": True}


@f_api.get("/cart", response_class=HTMLResponse) # GET Запрос от WEB - сервера
async def get_cart(request: Request):
    user_id = request.query_params.get("user_id")
    user_cart = server_cart.setdefault(int(user_id), [])
    print('user_cart = ', user_cart)
    total_price = sum(item['price'] for item in user_cart)
    return templates.TemplateResponse("cart.html",
    {"request": request, "cart": user_cart, "total_price": total_price})



@f_api.post("/reset-cart")
async def reset_cart(request: Request):
    data = await request.json()
    user_id = data.get("user_id")  # Получаем ID пользователя из запроса

    if user_id is None:
        return {"success": False, "error": "Telegram ID не передан"}

    temp = server_cart.setdefault(user_id, [])
    temp.clear()
    return {"success": True}


