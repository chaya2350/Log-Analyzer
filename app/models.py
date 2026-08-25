from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogEvent:
    timestamp: datetime
    level: str
    message: str