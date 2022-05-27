from fastapi import APIRouter
from config.db import conn
from models.admin import admins
from schemas.admin import Admin
from cryptography.fernet import Fernet

admin = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)


@admin.get("/admins", tags=["Admins"])
def get_admins():
    query = admins.select()
    result = conn.execute(query).fetchall()
    return result


@admin.get("/admins/{id}", tags=["Admins"])
def get_admin_by_id(admin_id: int):
    query = admins.select().where(admins.c.userID == admin_id)
    result = conn.execute(query).fetchone()
    if result is None:
        return {"message": "Admin not found"}
    return {"message": "Admin found", "User": result}


@admin.post("/admins", tags=["Admins"])
def create_admin(add_admin: Admin):
    new_password = f.encrypt(add_admin.password.encode("utf-8"))
    query = admins.insert().values(name=add_admin.name,
                                  email=add_admin.email,
                                  password=new_password)
    is_added = conn.execute(query)

    if is_added:
        return {"message": "Admin created successfully"}
    else:
        return {"message": "Admin not created"}


@admin.put("/admins/{id}", tags=["Admins"])
def update_admin(admin_id: int, admin_to_update: Admin):
    found_admin = conn.execute(admins.select().where(admins.c.userID == admin_id)).fetchone()

    if admin_to_update.name is None or admin_to_update.name == "string":
        admin_to_update.name = found_admin.name
    if admin_to_update.email is None or admin_to_update.email == "string":
        admin_to_update.email = found_admin.email
    if admin_to_update.password is None or admin_to_update.password == "string":
        admin_to_update.password = found_admin.password

    query = admins.update().where(admins.c.userID == admin_id).values(
        name=admin_to_update.name,
        email=admin_to_update.email,
        password=f.encrypt(admin_to_update.password.encode("utf-8"))
    )
    is_updated = conn.execute(query)

    if is_updated:
        return {"message": "Admin updated successfully"}
    else:
        return {"message": "Admin not updated"}


@admin.delete("/admins/{id}", tags=["Admins"])
def delete_admin(admin_id: int):
    query = admins.delete().where(admins.c.userID == admin_id)
    is_deleted = conn.execute(query)

    if is_deleted:
        return {"message": "Admin deleted successfully"}
    else:
        return {"message": "Admin not deleted"}
