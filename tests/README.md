# VersePad Tests

This directory contains unit tests for the VersePad application.

## Running the Tests

You can run the tests using the following command from the tests directory:

```bash
python run_tests.py
```

Or using pytest from the project root directory:

```bash
pytest
```

## Test Coverage

The tests cover the following functionality:

1. `setup_nltk` function - Tests the NLTK setup process
2. `get_word_at_cursor` method - Tests word extraction at different cursor positions
3. `get_rhyming_phrases` method - Tests generation of rhyming phrases
4. `get_near_rhymes` method - Tests finding near rhymes for words
5. `update_dictionary` method - Tests dictionary lookup and spelling suggestions

## Adding New Tests

To add new tests, follow these steps:

1. Add new test methods to the existing test classes in `test_versepad.py`
2. Ensure proper mocking of external dependencies
3. Run the tests to verify they pass

## Mock Strategy

The tests use Python's `unittest.mock` to mock external dependencies like Kivy, NLTK, and other libraries. This allows testing the application logic without requiring the actual UI framework or external resources.