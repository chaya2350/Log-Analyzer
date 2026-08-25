from dataclasses import asdict

from fastapi import (FastAPI, File, Form, HTTPException, UploadFile, Query)
from .parser import parse_file, parse_content
from .analyzer import analyze, search_events

app = FastAPI(title="Log Analyzer")

LOG_PATH = "logs/sample.log"

events = parse_file(LOG_PATH, "application")

@app.get("/summary")
def summary(
    log_type: str = Query(
        default="application",
        pattern="^(application|json|apache)$",
    )
):
    try:
        events = parse_file(LOG_PATH, log_type)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    return analyze(events)


@app.get("/events")
def get_events(
    log_type: str = Query(
        default="application",
        pattern="^(application|json|apache)$",
    ),
    query: str | None = None,
    level: str | None = None,
):
    events = parse_file(LOG_PATH, log_type)

    filtered = search_events(
        events,
        query=query,
        level=level,
    )

    return [
        {
            "timestamp": event.timestamp,
            "level": event.level,
            "message": event.message,
        }
        for event in filtered
    ]


@app.get("/events/{index}")
def get_event(index: int):
    if index < 0 or index >= len(events):
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    return asdict(events[index])


@app.post("/upload")
async def upload_log(
    file: UploadFile = File(...),
    log_type: str = Query(
        default="application",
        pattern="^(application|json|apache)$",
    ),
):
    content = await file.read()

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be UTF-8 encoded",
        )

    try:
        events = parse_content(text, log_type)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    result = analyze(events)

    return {
        "filename": file.filename,
        "log_type": log_type,
        **result,
    }


@app.get("/")
def root():
    return {
        "message": "Log Analyzer API",
        "docs": "/docs",
        "summary": "/summary",
        "events": "/events",
    }