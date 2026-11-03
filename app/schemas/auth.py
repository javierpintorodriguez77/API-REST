from pydantic import BaseModel, EmailStr, Field, model_validator


class UsuarioRegistro(BaseModel):
    email: EmailStr
    nombre: str = Field(min_length=3, max_length=100)
    telefono: str | None = Field(default=None, max_length=30)
    password: str = Field(min_length=8, max_length=64)
    confirmar_password: str

    @model_validator(mode="after")
    def validar_password(self):
        if self.password != self.confirmar_password:
            raise ValueError("Las contraseñas no coinciden")
        if not any(c.isupper() for c in self.password) or not any(c.islower() for c in self.password) or not any(c.isdigit() for c in self.password):
            raise ValueError("La contraseña debe incluir mayúscula, minúscula y número")
        return self


class TokenRespuesta(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


class CambioPassword(BaseModel):
    password_actual: str
    password_nueva: str = Field(min_length=8, max_length=64)

