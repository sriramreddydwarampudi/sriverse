# VersePad Pro

VersePad Pro is a poetry writing application built with Kivy. It provides real-time feedback on rhymes, meter, dictionary lookups, and more to help poets craft their verses.

## Features

- Real-time rhyme suggestions
- Meter analysis
- Dictionary lookups
- Grammar and style checking
- Thesaurus integration
- Save and load poems

## Requirements

- Python 3.x
- Kivy 2.3.0
- NLTK
- Pronouncing

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Building for Android

Use Buildozer to package the application for Android:

```bash
buildozer android debug
```

## Testing

The application includes unit tests to ensure functionality. To run the tests:

```bash
cd tests
python run_tests.py
```

Or using pytest from the project root:

```bash
pytest
```

See the [tests/README.md](tests/README.md) file for more information about testing.