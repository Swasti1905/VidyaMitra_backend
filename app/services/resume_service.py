from pathlib import Path

from sqlalchemy.orm import Session

from app.ai_modules.resume_parser import parse_resume
from app.config import get_settings
from app.models.resume import Resume
from app.models.user import User
from app.utils.files import build_storage_path, validate_upload


settings = get_settings()


def process_resume_upload(db: Session, user: User, upload_file) -> Resume:
    extension, content = validate_upload(upload_file, settings.max_upload_size_mb)
    storage_path = build_storage_path(settings.absolute_upload_dir, extension)
    storage_path.write_bytes(content)

    parsed = parse_resume(Path(storage_path))
    resume = Resume(
        user_id=user.id,
        filename=upload_file.filename or storage_path.name,
        storage_path=str(storage_path),
        raw_text=parsed["raw_text"],
        sections=parsed["sections"],
        extracted_skills=parsed["extracted_skills"],
        soft_skills=parsed["soft_skills"],
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume
