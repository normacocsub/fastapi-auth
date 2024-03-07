from pydantic import BaseModel


class RoleBase(BaseModel):
    nombre: str
    descripcion: str