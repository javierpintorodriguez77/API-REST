import json

import cloudinary
import cloudinary.api
import cloudinary.uploader
from cloudinary import CloudinaryImage
from dotenv import load_dotenv


# Carga CLOUDINARY_URL desde el archivo .env antes de configurar el SDK.
load_dotenv()

# El SDK lee CLOUDINARY_URL y genera URLs seguras (https).
config = cloudinary.config(secure=True)

print("****1. Configurar el SDK:****")
print("Cloud Name:", config.cloud_name)


def upload_image() -> None:
    """Sube una imagen de ejemplo y muestra su URL de entrega."""
    cloudinary.uploader.upload(
        "https://cloudinary-devs.github.io/cld-docs-assets/assets/images/butterfly.jpeg",
        public_id="quickstart_butterfly",
        unique_filename=False,
        overwrite=True,
    )

    src_url = CloudinaryImage("quickstart_butterfly").build_url()
    print("****2. Subir una imagen****")
    print("URL de entrega:", src_url)


def get_asset_info() -> None:
    """Consulta los metadatos y asigna una etiqueta según el ancho."""
    image_info = cloudinary.api.resource("quickstart_butterfly")
    print("****3. Obtener detalles de la imagen****")
    print(json.dumps(image_info, indent=2))

    width = image_info.get("width", 0)
    if width > 900:
        tag = "large"
    elif width > 500:
        tag = "medium"
    else:
        tag = "small"

    update_response = cloudinary.api.update(
        "quickstart_butterfly",
        tags=tag,
    )
    print("Nueva etiqueta asignada:", update_response.get("tags"))


def create_transformation() -> None:
    """Genera una URL con una transformación de tamaño y recorte."""
    transformed_url = CloudinaryImage("quickstart_butterfly").build_url(
        width=100,
        height=150,
        crop="fill",
    )
    print("****4. Transformar la imagen****")
    print("URL transformada:", transformed_url)


def main() -> None:
    upload_image()
    get_asset_info()
    create_transformation()


if __name__ == "__main__":
    main()
