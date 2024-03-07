from typing import Type
from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.role import get_role_by_name
from app.auth import encrypt_password


def get_user_by_email(email: str, db: Session) -> Type[User]:
    return db.query(User).filter_by(email=email).options(
        joinedload(User.roles)
    ).first()


def get_user_by_id(user_id: int, db: Session) -> Type[User]:
    return (db.query(User).filter_by(id=user_id).options(
        joinedload(User.roles)
    ).first())


def create_user(user: UserCreate, db: Session) -> User:
    db_user = User(email=user.email, hashed_password=encrypt_password(user.password), full_name=user.full_name)
    role = get_role_by_name(name='Usuario', db=db)
    if role:
        db_user.roles.append(role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    del db_user.hashed_password
    return db_user


def update_user(user: UserUpdate, user_id: int, db: Session) -> Type[User] | None:
    user_bd = get_user_by_id(user_id, db)
    if user_bd is None:
        return user_bd
    user_bd.email = user.email
    user_bd.full_name = user.full_name
    db.commit()
    db.refresh(user_bd)
    del user_bd.hashed_password
    return user_bd


def update_password(user: UserUpdate, user_id: int,  db: Session):
    user_bd = get_user_by_id(user_id, db)
    if user_bd is None:
        return user_bd
    user_bd.hashed_password = encrypt_password(user.password)
    db.commit()
    db.refresh(user_bd)
    del user_bd.hashed_password
    return user_bd

def delete_user(user_id: int, db: Session):
    user_bd = get_user_by_id(user_id, db)
    if user_bd is None:
        return user_bd
    db.delete(user_bd)
    db.commit()
    return {"message": "Usuario eliminado"}



