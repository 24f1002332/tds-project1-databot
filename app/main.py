from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.telegram_bot import create_bot

telegram_bot = create_bot()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await telegram_bot.initialize()
    await telegram_bot.start()
    await telegram_bot.updater.start_polling()

    yield

    await telegram_bot.updater.stop()
    await telegram_bot.stop()
    await telegram_bot.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/run.jsonl")
def run_log():
    log_file = Path("logs/run.jsonl")

    if not log_file.exists():
        log_file.touch()

    return FileResponse(
        log_file,
        media_type="application/json",
        filename="run.jsonl",
    )