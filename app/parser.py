from .log_parsers import (
    parse_application,
    parse_json,
    parse_apache,
)

from .models import LogEvent

PARSERS = {
    "application": parse_application,
    "json": parse_json,
    "apache": parse_apache,
}

def get_parser(log_type: str):
    parser = PARSERS.get(log_type.lower())

    if parser is None:
        raise ValueError(
            f"Unsupported log type: {log_type}"
        )

    return parser

def parse_content(content: str, log_type: str) -> list[LogEvent]:
    parser = get_parser(log_type)

    events = []

    for line in content.splitlines():
        event = parser(line)

        if event:
            events.append(event)

    return events

def parse_file(
    path: str,
    log_type: str,
) -> list[LogEvent]:
    parser = get_parser(log_type)

    events = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            event = parser(line)

            if event:
                events.append(event)

    return events