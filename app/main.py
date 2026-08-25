from dataclasses import asdict

from fastapi import FastAPI, HTTPException, Query

from .parser import parse_file
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


@app.get("/")
def root():
    return {
        "message": "Log Analyzer API",
        "docs": "/docs",
        "summary": "/summary",
        "events": "/events",
    }