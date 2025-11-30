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
    file_bytes = await file.read()

    filename = f"public/{file.filename}"

    try:
        supabase.storage.from_(SUPABASE_BUCKET).upload(
            path=filename,
            file=file_bytes,
            file_options={
                "content_type": file.content_type,
                "upsert": True
            }
        )
    except Exception:
        supabase.storage.from_(SUPABASE_BUCKET).update(
            path=filename,
            file=file_bytes,
            file_options={
                "content_type": file.content_type
            }
        )

    public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(filename)

    return public_url
