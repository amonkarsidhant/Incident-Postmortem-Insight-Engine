from pathlib import Path
from fastapi import FastAPI

from app.api.routes.postmortems import router as postmortem_router
from app.config import get_settings
from app.database import Base, engine


app = FastAPI(title="Incident Postmortem Insight Engine")
app.include_router(postmortem_router)


@app.on_event("startup")
async def on_startup() -> None:
    settings = get_settings()
    Path(settings.storage_dir).mkdir(parents=True, exist_ok=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
