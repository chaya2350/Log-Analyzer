# Log Analyzer

## Overview

Log Analyzer is a Python-based API for parsing and analyzing log files from multiple formats.

The project converts different log formats into a unified `LogEvent` model and provides analysis through a FastAPI REST API.

## Supported Log Formats

* Application logs
* JSON logs
* Apache access logs

All supported formats are normalized into:

```python
LogEvent(
    timestamp=datetime,
    level=str,
    message=str,
)
```

This allows the analysis layer to work independently of the original log format.

## Features

* Parse multiple log formats
* Normalize logs into a common data model
* Count log levels
* Find the most common errors
* Analyze errors by hour
* Search events by message
* Filter events by log level
* Upload log files through an API
* Generate summary statistics
* Interactive API documentation through Swagger

## Project Structure

```text
log-analyzer/
│
├── app/
│   ├── main.py
│   ├── parser.py
│   ├── log_parsers.py
│   ├── analyzer.py
│   └── models.py
│
├── logs/
│   └── sample.log
│
├── requirements.txt
└── README.md
```

### `models.py`

Defines the common `LogEvent` data model.

### `log_parsers.py`

Contains parsers for the supported log formats.

### `parser.py`

Selects the appropriate parser and converts log files or text content into `LogEvent` objects.

### `analyzer.py`

Contains the analysis logic:

* Log level statistics
* Common errors
* Errors by hour
* Event search

### `main.py`

Exposes the functionality through a FastAPI REST API.

## Installation

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Start the application with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### `GET /`

Returns basic API information.

### `GET /summary`

Analyzes the sample log file.

Example:

```text
GET /summary?log_type=application
```

Supported values:

```text
application
json
apache
```

### `GET /events`

Returns parsed events and supports filtering.

Search by message:

```text
GET /events?query=database
```

Filter by level:

```text
GET /events?level=ERROR
```

Combine filters:

```text
GET /events?level=ERROR&query=timeout
```

### `POST /upload`

Uploads and analyzes a log file.

The log type can be specified using:

```text
application
json
apache
```

The endpoint returns the filename, log type, and calculated statistics.

## Example Application Log

```text
2026-08-01T10:00:01 ERROR Database timeout
2026-08-01T10:01:15 INFO User logged in
2026-08-01T10:02:30 WARN Memory usage high
2026-08-01T10:03:12 ERROR Database timeout
```

The analyzer can produce statistics such as:

```json
{
  "total_lines": 4,
  "levels": {
    "ERROR": 2,
    "WARN": 1,
    "INFO": 1
  }
}
```

## Architecture

The project separates parsing from analysis:

```text
Log File
   │
   ▼
Parser
   │
   ▼
LogEvent[]
   │
   ▼
Analyzer
   │
   ▼
Statistics / Search Results
   │
   ▼
FastAPI
```

Each log format has its own parser, while the analyzer operates only on the common `LogEvent` model.

This makes it possible to add additional log formats without changing the analysis logic.

## Technologies

* Python
* FastAPI
* Uvicorn
* Pydantic / FastAPI validation
* Python `dataclasses`
* Regular Expressions
* JSON
* `collections.Counter`

## Future Improvements

Possible extensions include:

* Unit tests for all parsers and analyzer functions
* Support for additional log formats
* Detection and reporting of invalid log lines
* Persistent storage with SQLite
* Visualization dashboard
* Log upload history
* Automatic log format detection
* More advanced anomaly detection
