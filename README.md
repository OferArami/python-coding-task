# Anecdotes DummyJSON Plugin

This plugin collects evidence from the DummyJSON API for the Anecdotes platform.

## Features

- Connectivity testing with DummyJSON API
- Evidence collection:
  - E1: User details
  - E2: List of posts
  - E3: List of posts with comments

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

## Usage

Run the plugin:
```bash
python3 main.py
```

The plugin will:
1. Test connectivity with the API
2. Collect all required evidence
3. Print the collected evidence in JSON format

## Error Handling

The plugin handles various API errors and provides meaningful error messages for:
- Authentication failures
- Resource not found
- General API errors
