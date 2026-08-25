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


def parse_file(path: str, log_type: str) -> list:
    parser = PARSERS.get(log_type.lower())

    if parser is None:
        raise ValueError(
            f"Unsupported log type: {log_type}"
        )

    events = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            event = parser(line)

            if event:
                events.append(event)

    return events