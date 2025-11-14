import os
from pathlib import Path
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_session
from app.models import Postmortem
from app.schemas import PostmortemRead
from services.evaluator import evaluate_postmortem


router = APIRouter(prefix="/api/v1/postmortems", tags=["postmortems"])


def _ensure_storage_dir(path: str) -> Path:
    storage_path = Path(path)
    storage_path.mkdir(parents=True, exist_ok=True)
    return storage_path


@router.post("", response_model=PostmortemRead, status_code=status.HTTP_201_CREATED)
async def create_postmortem(
    owner: Annotated[str, Form(...)],
    file: Annotated[UploadFile, File(...)],
    session: AsyncSession = Depends(get_session),
):
    settings = get_settings()
    storage_path = _ensure_storage_dir(settings.storage_dir)

    file_contents = await file.read()
    file_id = os.urandom(16).hex()
    target_path = storage_path / f"{file_id}_{file.filename}"
    with target_path.open("wb") as buffer:
        buffer.write(file_contents)

    postmortem = Postmortem(owner=owner, file_path=str(target_path))
    session.add(postmortem)
    await session.commit()
    await session.refresh(postmortem)
    return PostmortemRead.from_orm(postmortem)


@router.get("/{postmortem_id}", response_model=PostmortemRead)
async def get_postmortem(postmortem_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Postmortem).where(Postmortem.id == postmortem_id))
    postmortem = result.scalar_one_or_none()
    if postmortem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Postmortem not found")
    return PostmortemRead.from_orm(postmortem)


@router.post("/{postmortem_id}/curate", response_model=PostmortemRead)
async def curate_postmortem(postmortem_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Postmortem).where(Postmortem.id == postmortem_id))
    postmortem = result.scalar_one_or_none()
    if postmortem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Postmortem not found")

    evaluation = evaluate_postmortem(postmortem.file_path)
    postmortem.evaluator_json = evaluation
    session.add(postmortem)
    await session.commit()
    await session.refresh(postmortem)
    return PostmortemRead.from_orm(postmortem)
