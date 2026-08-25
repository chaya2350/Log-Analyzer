from .log_parsers import (
    parse_application,
    parse_json,
    parse_apache,
)


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

def parse_content(content: str, log_type: str) -> list[LogEvent]:
    parser = get_parser(log_type)

    events = []

    for line in content.splitlines():
        event = parser(line)

        if event:
            events.append(event)

    return events