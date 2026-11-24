from app.core.config import get_settings


def _configurar():
    """Carga y configura el SDK solo cuando se necesita una operación de imagen."""
    try:
        import cloudinary
    except ImportError as error:
        raise RuntimeError("La dependencia cloudinary no está instalada") from error

    settings = get_settings()
    if settings.cloudinary_url:
        cloudinary.config(cloudinary_url=settings.cloudinary_url, secure=True)
    elif all((settings.cloudinary_cloud_name, settings.cloudinary_api_key, settings.cloudinary_api_secret)):
        cloudinary.config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True,
        )
    else:
        raise RuntimeError("Cloudinary no está configurado")
    return cloudinary


def subir_portada(contenido: bytes, libro_id: int) -> str:
    """Sube una portada y devuelve la URL segura que debe guardarse en el libro."""
    cloudinary = _configurar()
    resultado = cloudinary.uploader.upload(
        contenido,
        folder="biblioteca/portadas",
        public_id=f"libro_{libro_id}",
        overwrite=True,
        resource_type="image",
    )
    return str(resultado["secure_url"])

