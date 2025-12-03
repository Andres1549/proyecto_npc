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
    content = await file.read()

    ext = file.filename.split(".")[-1]
    filename = f"public/{uuid.uuid4()}.{ext}"

    res = supabase.storage.from_(SUPABASE_BUCKET).upload(
        path=filename,
        file=content,
        file_options={
            "content-type": file.content_type
        }
    )

    if getattr(res, "error", None):
        supabase.storage.from_(SUPABASE_BUCKET).update(
            path=filename,
            file=content,
            file_options={
                "content-type": file.content_type
            }
        )

    public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(filename)
    return public_url
