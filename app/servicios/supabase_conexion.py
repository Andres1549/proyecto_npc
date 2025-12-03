import os
import uuid
from fastapi import UploadFile
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def upload_file(file: UploadFile) -> str:
    if not file:
        return None  # No hay archivo

    content = await file.read()

    if not content:
        return None  # Archivo vacío

    filename = f"{uuid.uuid4()}_{file.filename}"

    supabase.storage.from_(SUPABASE_BUCKET).upload(
        path=filename,
        file=content,
        file_options={"content-type": file.content_type, "upsert": True}
    )

    url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{filename}"

    return url

