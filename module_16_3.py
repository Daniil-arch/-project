import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Dict

app = FastAPI()

# Инициализация словаря users
users: Dict[str, str] = {'1': 'Имя: Example, возраст: 18'}

@app.get("/users")
def read_users():
    return users

@app.post("/user/{username}/{age}")
def create_user(username: str, age: int):
    new_id = str(max(map(int, users.keys()), default=0) + 1)
    users[new_id] = f"Имя: {username}, возраст: {age}"
    return f"User {new_id} is registered"

@app.put("/user/{user_id}/{username}/{age}")
def update_user(user_id: str, username: str, age: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {user_id} has been updated"

@app.delete("/user/{user_id}")
def delete_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return f"User {user_id} has been deleted"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)