from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def validate_upload(upload: UploadFile, max_size_mb: int) -> tuple[str, bytes]:
    extension = Path(upload.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF and DOCX files are supported")

    content = upload.file.read()
    if len(content) > max_size_mb * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file exceeds configured size limit")

    return extension, content


def build_storage_path(base_dir: Path, extension: str) -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / f"{uuid4().hex}{extension}"
