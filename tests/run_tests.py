import unittest
import sys
import os

# Add the parent directory to the path so we can import the test modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the test modules
from test_versepad import TestSetupNltk, TestVersePad

if __name__ == '__main__':
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add the test cases using the newer TestLoader API
    loader = unittest.TestLoader()
    test_suite.addTests(loader.loadTestsFromTestCase(TestSetupNltk))
    test_suite.addTests(loader.loadTestsFromTestCase(TestVersePad))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with non-zero code if tests failed
    sys.exit(not result.wasSuccessful())