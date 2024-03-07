from fastapi import APIRouter, status, Depends, HTTPException
from app.services.role import (create_role, get_role_by_name, update_role,
                               delete_role, get_roles, get_role_by_id)
from app.schemas.Role import RoleBase
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_role(role: RoleBase, db: Session = Depends(get_db)):
    try:
        return create_role(role=role, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}"
        )


@router.put("/{role_id}")
def actualizar_role(role_id: int, role: RoleBase, db: Session = Depends(get_db)):
    try:
        role_db = update_role(role_id=role_id, role=role, db=db)
        if role_db is None:
            return JSONResponse(content={"message": "No se encontro"},
                                status_code=status.HTTP_404_NOT_FOUND)
        return role_db
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}"
        )


@router.delete("/{role_id}")
def eliminar_role(role_id: int, db: Session = Depends(get_db)):
    try:
        role_db = delete_role(role_id=role_id, db=db)
        if role_db is None:
            return JSONResponse(content={"message": "No se encontro"},
                                status_code=status.HTTP_404_NOT_FOUND)
        return role_db
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}"
        )


@router.get("/")
def obtener_roles(db: Session = Depends(get_db)):
    try:
        return get_roles(db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}"
        )


@router.get("/get_by_id/{role_id}")
def obtener_role_id(role_id: int, db: Session = Depends(get_db)):
    try:
        role = get_role_by_id(role_id=role_id, db=db)
        if role is None:
            return JSONResponse(content={"message": "No se encontro"},
                                status_code=status.HTTP_404_NOT_FOUND)
        return role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}"
        )


@router.get("/get_by_name/{name}")
def obtener_role_name(name: str, db: Session = Depends(get_db)):
    try:
        role = get_role_by_name(name=name, db=db)
        if role is None:
            return JSONResponse(content={"message": "No se encontro"},
                                status_code=status.HTTP_404_NOT_FOUND)
        return role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}"
        )
