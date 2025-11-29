import os
from supabase import create_client
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


async def upload_file(file: UploadFile) -> str:

    file_bytes = await file.read()

    filename = f"uploads/{file.filename}"

    try:
        res = supabase.storage.from_(SUPABASE_BUCKET).upload(
            path=filename,
            file=file_bytes,
            file_options={
                "content-type": file.content_type
            }
        )

        if "error" in res and "already exists" in str(res["error"]).lower():
            res = supabase.storage.from_(SUPABASE_BUCKET).update(
                path=filename,
                file=file_bytes,
                file_options={
                    "content-type": file.content_type
                }
            )

    except Exception as e:
        raise Exception(f"Error subiendo archivo: {str(e)}")

    url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(filename)

    return url
