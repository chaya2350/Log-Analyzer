from collections import Counter
from .models import LogEvent


def count_levels(events: list[LogEvent]) -> dict[str, int]:
    counter = Counter(event.level for event in events)

    return {
        "ERROR": counter.get("ERROR", 0),
        "WARN": counter.get("WARN", 0),
        "INFO": counter.get("INFO", 0),
    }


def most_common_errors(
    events: list[LogEvent],
    limit: int = 10,
) -> list[tuple[str, int]]:
    errors = [
        event.message
        for event in events
        if event.level == "ERROR"
    ]

    return Counter(errors).most_common(limit)


def errors_by_hour(events: list[LogEvent]) -> dict[int, int]:
    counter = Counter(
        event.timestamp.hour
        for event in events
        if event.level == "ERROR"
    )

    return dict(sorted(counter.items()))


def search_events(
    events: list[LogEvent],
    query: str | None = None,
    level: str | None = None,
) -> list[LogEvent]:
    result = events

    if level:
        result = [
            event
            for event in result
            if event.level == level
        ]

    if query:
        query = query.lower()

        result = [
            event
            for event in result
            if query in event.message.lower()
        ]

    return result


def analyze(events: list[LogEvent]) -> dict:
    return {
        "total_lines": len(events),
        "levels": count_levels(events),
        "common_errors": most_common_errors(events),
        "errors_by_hour": errors_by_hour(events),
    }