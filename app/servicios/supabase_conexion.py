import os
from fastapi import UploadFile
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


async def upload_file(file: UploadFile) -> str:
    # Leer bytes
    file_bytes = await file.read()

    # Ruta real dentro del bucket
    filename = f"public/{file.filename}"

    # Intentar subir
    res = supabase.storage.from_(SUPABASE_BUCKET).upload(
        path=filename,
        file=file_bytes,
        file_options={
            "content-type": file.content_type,
        }
    )

    # 🔍 Si hay error en upload
    if getattr(res, "error", None):
        # Intentar update (equivalente a upsert válido)
        res = supabase.storage.from_(SUPABASE_BUCKET).update(
            path=filename,
            file=file_bytes,
            file_options={
                "content-type": file.content_type,
            }
        )

        if getattr(res, "error", None):
            raise Exception(f"Error subiendo archivo: {res.error}")

    # Obtener URL pública
    public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(filename)

    return public_url
