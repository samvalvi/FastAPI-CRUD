from fastapi import APIRouter
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet

user = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)


@user.get("/users", tags=["Users"])
def get_users():
    query = users.select()
    result = conn.execute(query).fetchall()
    return result


@user.get("/users/{id}", tags=["Users"])
def get_user_by_id(user_id: int):
    query = users.select().where(users.c.userID == user_id)
    result = conn.execute(query).fetchone()
    if result is None:
        return {"message": "User not found"}
    return {"message": "User found", "User": result}


@user.post("/users", tags=["Users"])
def create_user(add_user: User):
    new_password = f.encrypt(add_user.password.encode("utf-8"))
    query = users.insert().values(name=add_user.name,
                                  email=add_user.email,
                                  password=new_password)
    is_added = conn.execute(query)

    if is_added:
        return {"message": "User created successfully"}
    else:
        return {"message": "User not created"}


@user.put("/users/{id}", tags=["Users"])
def update_user(user_id: int, user_to_update: User):
    found_user = conn.execute(users.select().where(users.c.userID == user_id)).fetchone()

    if user_to_update.name is None or user_to_update.name == "string":
        user_to_update.name = found_user.name
    if user_to_update.email is None or user_to_update.email == "string":
        user_to_update.email = found_user.email
    if user_to_update.password is None or user_to_update.password == "string":
        user_to_update.password = found_user.password

    query = users.update().where(users.c.userID == user_id).values(
        name=user_to_update.name,
        email=user_to_update.email,
        password=f.encrypt(user_to_update.password.encode("utf-8"))
    )
    is_updated = conn.execute(query)

    if is_updated:
        return {"message": "User updated successfully"}
    else:
        return {"message": "User not updated"}


@user.delete("/users/{id}", tags=["Users"])
def delete_user(user_id: int):
    query = users.delete().where(users.c.userID == user_id)
    is_deleted = conn.execute(query)

    if is_deleted:
        return {"message": "User deleted successfully"}
    else:
        return {"message": "User not deleted"}
