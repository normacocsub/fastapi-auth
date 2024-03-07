from fastapi import APIRouter, status, Depends, HTTPException, Security
from app.schemas.user import UserCreate, UserUpdate
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth_utils import auth_required
from app.services.user import (get_user_by_email, create_user, get_user_by_id,
                               update_user, delete_user, update_password)

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def registrar_usuario(user: UserCreate, db: Session = Depends(get_db),
                      token: str = Security(auth_required(["Admin"]))):
    try:
        db_user = get_user_by_email(email=user.email, db=db)
        if db_user:
            return JSONResponse(
                content={"message": "El correo se encuentra registrado"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        return create_user(user=user, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )



@router.get("/get_by_email/{email}")
def obtener_usuario_email(email: str, db: Session = Depends(get_db),
                          token: str = Security(auth_required(["Admin", "Usuario"]))):
    try:
        db_user = get_user_by_email(email=email, db=db)
        if db_user is None:
            return JSONResponse(
                content={"message": "No se encontro el usuario"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        del db_user.hashed_password
        return db_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


@router.get("/get_by_id/{user_id}")
def obtener_usuario_id(user_id: int, db: Session = Depends(get_db),
                       token: str = Security(auth_required(["Admin", "Usuario"]))):
    try:
        db_user = get_user_by_id(user_id=user_id, db=db)
        if db_user is None:
            return JSONResponse(
                content={"message": "No se encontro el usuario"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        del db_user.hashed_password
        return db_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


@router.put("/{user_id}")
def actualizar_usuario(user_id: int, user: UserUpdate, db: Session = Depends(get_db),
                       token: str = Security(auth_required(["Admin", "Usuario"]))):
    try:
        db_user = update_user(user_id=user_id, user=user, db=db)
        if db_user is None:
            return JSONResponse(
                content={"message": "No se encontro el usuario"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        return db_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


@router.put("/update_password/{user_id}")
def cambiar_password(user_id: int, user: UserUpdate, db: Session = Depends(get_db),
                     token: str = Security(auth_required(["Admin", "Usuario"]))):
    try:
        user = update_password(user_id=user_id, user=user, db=db)
        if user is None:
            return JSONResponse(
                content={"message": "No se encontro el usuario"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


@router.delete("/{user_id}")
def eliminar_usuario(user_id: int, db: Session = Depends(get_db),
                     token: str = Security(auth_required(["Admin", "Usuario"]))):
    try:
        db_user = delete_user(user_id=user_id, db=db)
        if db_user is None:
            return JSONResponse(
                content={"message": "No se encontro el usuario"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        return db_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )
