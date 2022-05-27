from fastapi import FastAPI
from routes.user import user
from routes.admin import admin

app = FastAPI(
    title="User API",
    description="This is a user API",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "Users",
            "description": "User related operations"
        },
        {
            "name": "Admins",
            "description": "Admin related operations"
        }
    ]
)

app.include_router(user)
app.include_router(admin)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
