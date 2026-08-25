import json
import re
from datetime import datetime

from .models import LogEvent


APPLICATION_PATTERN = re.compile(
    r"^(?P<timestamp>\S+)\s+"
    r"(?P<level>ERROR|WARN|INFO)\s+"
    r"(?P<message>.*)$"
)


APACHE_PATTERN = re.compile(
    r'^(?P<ip>\S+)\s+\S+\s+\S+\s+'
    r'\[(?P<timestamp>[^\]]+)\]\s+'
    r'"(?P<method>\S+)\s+(?P<path>\S+)\s+\S+"\s+'
    r'(?P<status>\d+)\s+(?P<size>\S+)'
)


def parse_application(line: str) -> LogEvent | None:
    match = APPLICATION_PATTERN.match(line.strip())

    if not match:
        return None

    return LogEvent(
        timestamp=datetime.fromisoformat(match.group("timestamp")),
        level=match.group("level"),
        message=match.group("message"),
    )


def parse_json(line: str) -> LogEvent | None:
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return None

    timestamp = data.get("timestamp")
    level = data.get("level", "INFO")
    message = data.get("message", "")

    if not timestamp:
        return None

    return LogEvent(
        timestamp=datetime.fromisoformat(timestamp),
        level=level,
        message=message,
    )


def parse_apache(line: str) -> LogEvent | None:
    match = APACHE_PATTERN.match(line.strip())

    if not match:
        return None

    status = int(match.group("status"))

    if status >= 500:
        level = "ERROR"
    elif status >= 400:
        level = "WARN"
    else:
        level = "INFO"

    timestamp = datetime.strptime(
        match.group("timestamp"),
        "%d/%b/%Y:%H:%M:%S %z",
    )

    message = (
        f'{match.group("method")} '
        f'{match.group("path")} '
        f'{status}'
    )

    return LogEvent(
        timestamp=timestamp,
        level=level,
        message=message,
    )