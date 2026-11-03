from getpass import getpass
from sqlalchemy import select
from app.core.database import SessionLocal
from app.core.security import hashear_password
from app.models.usuario import RolUsuario, Usuario


def main():
    db = SessionLocal()
    try:
        email = input("Email: ").strip().lower()
        if db.scalar(select(Usuario).where(Usuario.email == email)):
            print("El usuario ya existe")
            return
        user = Usuario(email=email, nombre=input("Nombre: ").strip().title(), password_hash=hashear_password(getpass("Contraseña: ")), rol=RolUsuario.admin)
        db.add(user); db.commit(); print("Administrador creado")
    finally:
        db.close()


if __name__ == "__main__": main()

