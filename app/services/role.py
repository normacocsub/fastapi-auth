from typing import Type
from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.Role import RoleBase


def get_role_by_name(name: str, db: Session) -> Type[Role]:
    return db.query(Role).filter_by(nombre=name).first()


def get_role_by_id(role_id: int, db: Session) -> Type[Role]:
    return db.query(Role).filter_by(id=role_id).first()


def get_roles(db: Session):
    return db.query(Role).all()


def create_role(role: RoleBase, db: Session) -> Type[Role] | dict:
    role_db = get_role_by_name(name=role.nombre, db=db)
    if role_db:
        return {"message": "Role exist"}
    role_model = Role(nombre=role.nombre, descripcion=role.descripcion)
    db.add(role_model)
    db.commit()
    db.refresh(role_model)
    return role_model


def update_role(role: RoleBase, db: Session, role_id: int):
    role_db = get_role_by_id(role_id=role_id, db=db)
    if role_db is None:
        return role_db
    role_db.nombre = role.nombre
    role_db.descripcion = role.descripcion
    db.commit()
    db.refresh(role_db)
    return role_db


def delete_role(role_id: int, db: Session):
    role_db = get_role_by_id(role_id=role_id, db=db)
    if role_db is None:
        return role_db
    db.delete(role_db)
    db.commit()
    return {"mensaje": "Se elimino el role"}
