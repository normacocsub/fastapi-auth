from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.role import router as role_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "La aplicacion esta funcionando"}


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(role_router, prefix="/role", tags=["role"])
