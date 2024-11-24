import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Query
from typing import Annotated
from pydantic import constr, conint

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return "Главная страница"

@app.get("/user/admin", response_class=HTMLResponse)
def read_admin():
    return "Вы вошли как администратор"

@app.get("/user/{user_id}", response_class=HTMLResponse)
def read_user(
    user_id: Annotated[
        conint(ge=1, le=100),  # Ограничение: больше или равно 1 и меньше или равно 100
        Path(description="Enter User ID", example=1)
    ]
):
    return f"Вы вошли как пользователь № {user_id}"

@app.get("/user/{username}/{age}", response_class=HTMLResponse)
def read_user_info(
    username: Annotated[
        constr(min_length=5, max_length=20),  # Ограничение длины username
        Path(description="Enter username", example="UrbanUser")
    ],
    age: Annotated[
        conint(ge=18, le=120),  # Ограничение: больше или равно 18 и меньше или равно 120
        Path(description="Enter age", example=24)
    ]
):
    return f"Информация о пользователе. Имя: {username}, Возраст: {age}"