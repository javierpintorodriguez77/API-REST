from fastapi import HTTPException, status


class NoAutenticado(HTTPException):
    def __init__(self, detail: str = "No autenticado"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers={"WWW-Authenticate": "Bearer"})


class Prohibido(HTTPException):
    def __init__(self, detail: str = "No tiene permisos para esta acción"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class CuentaBloqueada(HTTPException):
    def __init__(self, detail: str = "Cuenta bloqueada temporalmente"):
        super().__init__(status_code=423, detail=detail)

