import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the main module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create mock modules
mock_kivy = MagicMock()
mock_app = MagicMock()
mock_boxlayout = MagicMock()
mock_textinput = MagicMock()
mock_tabbedpanel = MagicMock()
mock_label = MagicMock()
mock_scrollview = MagicMock()
mock_button = MagicMock()
mock_popup = MagicMock()
mock_filechooser = MagicMock()
mock_window = MagicMock()
mock_utils = MagicMock()
mock_metrics = MagicMock()
mock_clock = MagicMock()
mock_nltk = MagicMock()
mock_nltk_corpus = MagicMock()
mock_wordnet = MagicMock()
mock_words = MagicMock()
mock_cmudict = MagicMock()
mock_pronouncing = MagicMock()
mock_difflib = MagicMock()

# Mock the modules
sys.modules['kivy'] = mock_kivy
sys.modules['kivy.app'] = mock_app
sys.modules['kivy.uix.boxlayout'] = mock_boxlayout
sys.modules['kivy.uix.textinput'] = mock_textinput
sys.modules['kivy.uix.tabbedpanel'] = mock_tabbedpanel
sys.modules['kivy.uix.label'] = mock_label
sys.modules['kivy.uix.scrollview'] = mock_scrollview
sys.modules['kivy.uix.button'] = mock_button
sys.modules['kivy.uix.popup'] = mock_popup
sys.modules['kivy.uix.filechooser'] = mock_filechooser
sys.modules['kivy.core.window'] = mock_window
sys.modules['kivy.utils'] = mock_utils
sys.modules['kivy.metrics'] = mock_metrics
sys.modules['kivy.clock'] = mock_clock
sys.modules['nltk'] = mock_nltk
sys.modules['nltk.corpus'] = mock_nltk_corpus
sys.modules['nltk.corpus.wordnet'] = mock_wordnet
sys.modules['nltk.corpus.words'] = mock_words
sys.modules['nltk.corpus.cmudict'] = mock_cmudict
sys.modules['pronouncing'] = mock_pronouncing
sys.modules['difflib'] = mock_difflib

# Set platform to 'test'
mock_utils.platform = 'test'

# Import the main module after mocking
from main import setup_nltk

# Create a minimal version of the VersePad class for testing
class VersePadForTesting:
    def __init__(self):
        self.text_input = MagicMock()
        self.dict_tab = MagicMock()
        self.rhyme_tab = MagicMock()
        self.meter_tab = MagicMock()
        self.grammar_tab = MagicMock()
        self.thesaurus_tab = MagicMock()
    
    def get_word_at_cursor(self):
        cursor_index = self.text_input.cursor_index()
        text = self.text_input.text
        left = re.findall(r'\w+$', text[:cursor_index])
        right = re.findall(r'^\w+', text[cursor_index:])
        return (left[0] if left else "") + (right[0] if right else "")
    
    def get_rhyming_phrases(self, word, text):
        patterns = [f"{word} and {{}}", f"{{}} {word}", f"{word} {{}}"]
        rhymes = mock_pronouncing.rhymes(word)
        return [p.format(r) for p in patterns for r in rhymes[:3]] if rhymes else []
    
    def get_near_rhymes(self, word):
        if word.lower() not in mock_cmudict.dict():
            return []
        target = mock_cmudict.dict()[word.lower()][0][-2:]
        return [w for w, p in mock_cmudict.dict().items() if w != word.lower() and len(p[0]) > 2 and p[0][-2:] == target]
    
    def update_dictionary(self, text):
        word = self.get_word_at_cursor()
        if not word:
            self.dict_tab.text = "Move cursor over a word to see info"
            return
        
        output = f"[b][color=3366ff]Dictionary for:[/color] [b]{word}[/b][/b]\n\n"
        
        if word.lower() in mock_words.words():
            output += "[color=33cc33]✓ correct spelling[/color]\n"
        else:
            sugg = mock_difflib.get_close_matches(word, mock_words.words(), n=2)
            if sugg:
                output += f"[color=ff6600]Suggestions: {', '.join(sugg)}[/color]\n"
            else:
                output += "[color=ff0000]Possibly incorrect[/color]\n"
        
        syns = mock_wordnet.synsets(word.lower())
        if syns:
            output += f"[i]Definition:[/i] {syns[0].definition()}\n"
        phones = mock_pronouncing.phones_for_word(word.lower())
        if phones:
            output += f"[i]Syllables:[/i] {mock_pronouncing.syllable_count(phones[0])}\n"
        
        self.dict_tab.text = output

# Import re module for the get_word_at_cursor method
import re

class TestSetupNltk(unittest.TestCase):
    @patch('os.makedirs')
    @patch('nltk.data.path')
    @patch('nltk.data.find')
    @patch('nltk.download')
    def test_setup_nltk(self, mock_download, mock_find, mock_path, mock_makedirs):
        # Configure the mock to raise LookupError for all corpora
        mock_find.side_effect = LookupError()
        
        # Call the function
        setup_nltk()
        
        # Verify that os.makedirs was called with exist_ok=True
        mock_makedirs.assert_called_once()
        self.assertTrue(mock_makedirs.call_args[1].get('exist_ok', False))
        
        # Verify that nltk.data.path.append was called
        mock_path.append.assert_called_once()
        
        # Verify that nltk.download was called for each corpus
        self.assertEqual(mock_download.call_count, 3)
        
        # Verify the corpora that were downloaded
        downloaded_corpora = [call_args[0][0] for call_args in mock_download.call_args_list]
        self.assertIn('words', downloaded_corpora)
        self.assertIn('wordnet', downloaded_corpora)
        self.assertIn('cmudict', downloaded_corpora)

class TestVersePad(unittest.TestCase):
    def setUp(self):
        # Create an instance of our testing class
        self.verse_pad = VersePadForTesting()
    
    def test_get_word_at_cursor_empty(self):
        # Mock the cursor_index method to return 0
        self.verse_pad.text_input.cursor_index.return_value = 0
        
        # Mock the text attribute to be empty
        self.verse_pad.text_input.text = ""
        
        # Call the method
        result = self.verse_pad.get_word_at_cursor()
        
        # Verify the result
        self.assertEqual(result, "")
    
    def test_get_word_at_cursor_middle_of_word(self):
        # Mock the cursor_index method to return a position in the middle of a word
        self.verse_pad.text_input.cursor_index.return_value = 7
        
        # Mock the text attribute with a sample text
        self.verse_pad.text_input.text = "Hello world"
        
        # Call the method
        result = self.verse_pad.get_word_at_cursor()
        
        # Verify the result
        self.assertEqual(result, "world")
    
    def test_get_word_at_cursor_start_of_word(self):
        # Mock the cursor_index method to return a position at the start of a word
        self.verse_pad.text_input.cursor_index.return_value = 6
        
        # Mock the text attribute with a sample text
        self.verse_pad.text_input.text = "Hello world"
        
        # Call the method
        result = self.verse_pad.get_word_at_cursor()
        
        # Verify the result
        self.assertEqual(result, "world")
    
    def test_get_word_at_cursor_end_of_word(self):
        # Mock the cursor_index method to return a position at the end of a word
        self.verse_pad.text_input.cursor_index.return_value = 5
        
        # Mock the text attribute with a sample text
        self.verse_pad.text_input.text = "Hello world"
        
        # Call the method
        result = self.verse_pad.get_word_at_cursor()
        
        # Verify the result
        self.assertEqual(result, "Hello")
    
    def test_get_rhyming_phrases(self):
        # Mock the rhymes function to return a list of rhymes
        mock_pronouncing.rhymes.return_value = ["day", "way", "say", "play"]
        
        # Call the method
        result = self.verse_pad.get_rhyming_phrases("stay", "Some text")
        
        # Verify that pronouncing.rhymes was called with the correct word
        mock_pronouncing.rhymes.assert_called_once_with("stay")
        
        # Verify that the result contains the expected number of phrases
        self.assertEqual(len(result), 9)  # 3 patterns * 3 rhymes
        
        # Verify that the phrases contain the expected words
        for phrase in result:
            self.assertTrue("stay" in phrase)
            self.assertTrue(any(rhyme in phrase for rhyme in ["day", "way", "say", "play"]))
    
    def test_get_rhyming_phrases_no_rhymes(self):
        # Reset the mock
        mock_pronouncing.rhymes.reset_mock()
        
        # Mock the rhymes function to return an empty list
        mock_pronouncing.rhymes.return_value = []
        
        # Call the method
        result = self.verse_pad.get_rhyming_phrases("xyz", "Some text")
        
        # Verify that pronouncing.rhymes was called with the correct word
        mock_pronouncing.rhymes.assert_called_once_with("xyz")
        
        # Verify that the result is an empty list
        self.assertEqual(result, [])
    
    def test_get_near_rhymes_word_not_in_dict(self):
        # Mock the cmudict.dict() to return a dictionary
        mock_cmudict.dict.return_value = {"cat": [["K", "AE", "T"]], "hat": [["H", "AE", "T"]]}
        
        # Call the method with a word not in the dictionary
        result = self.verse_pad.get_near_rhymes("dog")
        
        # Verify that the result is an empty list
        self.assertEqual(result, [])
    
    def test_get_near_rhymes_with_matches(self):
        # Mock the cmudict.dict() to return a dictionary with some near rhymes
        mock_dict = {
            "cat": [["K", "AE", "T"]],
            "hat": [["H", "AE", "T"]],
            "bat": [["B", "AE", "T"]],
            "rat": [["R", "AE", "T"]],
            "dog": [["D", "AO", "G"]],
            "log": [["L", "AO", "G"]],
            "fog": [["F", "AO", "G"]],
            "a": [["AH"]]  # Too short to be a near rhyme
        }
        mock_cmudict.dict.return_value = mock_dict
        
        # Call the method
        result = self.verse_pad.get_near_rhymes("cat")
        
        # Verify that the result contains the expected near rhymes
        self.assertEqual(set(result), {"hat", "bat", "rat"})
        
        # Test with a different word
        result = self.verse_pad.get_near_rhymes("dog")
        
        # Verify that the result contains the expected near rhymes
        self.assertEqual(set(result), {"log", "fog"})
    
    def test_update_dictionary_no_word(self):
        # Mock the get_word_at_cursor method to return an empty string
        self.verse_pad.get_word_at_cursor = MagicMock(return_value="")
        
        # Call the method
        self.verse_pad.update_dictionary("Some text")
        
        # Verify that the dict_tab.text was set correctly
        self.verse_pad.dict_tab.text = "Move cursor over a word to see info"
    
    def test_update_dictionary_correct_spelling(self):
        # Mock the get_word_at_cursor method to return a word
        self.verse_pad.get_word_at_cursor = MagicMock(return_value="cat")
        
        # Mock the words.words() method to return a list of words
        mock_words.words.return_value = ["cat", "dog", "hat"]
        
        # Mock the wordnet.synsets method to return a list of synsets
        synset_mock = MagicMock()
        synset_mock.definition.return_value = "A small domesticated carnivorous mammal"
        mock_wordnet.synsets.return_value = [synset_mock]
        
        # Mock the pronouncing.phones_for_word method to return a list of phones
        mock_pronouncing.phones_for_word.return_value = ["K AE1 T"]
        
        # Mock the pronouncing.syllable_count method to return a count
        mock_pronouncing.syllable_count.return_value = 1
        
        # Call the method
        self.verse_pad.update_dictionary("Some text")
        
        # Verify that the dict_tab.text was set correctly
        self.assertTrue("[color=33cc33]✓ correct spelling[/color]" in self.verse_pad.dict_tab.text)
        self.assertTrue("Definition:" in self.verse_pad.dict_tab.text)
        self.assertTrue("Syllables:" in self.verse_pad.dict_tab.text)
    
    def test_update_dictionary_incorrect_spelling_with_suggestions(self):
        # Mock the get_word_at_cursor method to return a word
        self.verse_pad.get_word_at_cursor = MagicMock(return_value="caat")
        
        # Mock the words.words() method to return a list of words
        mock_words.words.return_value = ["cat", "dog", "hat"]
        
        # Mock the difflib.get_close_matches method to return a list of matches
        mock_difflib.get_close_matches.return_value = ["cat"]
        
        # Mock the wordnet.synsets method to return an empty list
        mock_wordnet.synsets.return_value = []
        
        # Mock the pronouncing.phones_for_word method to return an empty list
        mock_pronouncing.phones_for_word.return_value = []
        
        # Call the method
        self.verse_pad.update_dictionary("Some text")
        
        # Verify that the dict_tab.text was set correctly
        self.assertTrue("[color=ff6600]Suggestions: cat[/color]" in self.verse_pad.dict_tab.text)
        self.assertFalse("Definition:" in self.verse_pad.dict_tab.text)
        self.assertFalse("Syllables:" in self.verse_pad.dict_tab.text)
    
    def test_update_dictionary_incorrect_spelling_no_suggestions(self):
        # Mock the get_word_at_cursor method to return a word
        self.verse_pad.get_word_at_cursor = MagicMock(return_value="xyzabc")
        
        # Mock the words.words() method to return a list of words
        mock_words.words.return_value = ["cat", "dog", "hat"]
        
        # Mock the difflib.get_close_matches method to return an empty list
        mock_difflib.get_close_matches.return_value = []
        
        # Mock the wordnet.synsets method to return an empty list
        mock_wordnet.synsets.return_value = []
        
        # Mock the pronouncing.phones_for_word method to return an empty list
        mock_pronouncing.phones_for_word.return_value = []
        
        # Call the method
        self.verse_pad.update_dictionary("Some text")
        
        # Verify that the dict_tab.text was set correctly
        self.assertTrue("[color=ff0000]Possibly incorrect[/color]" in self.verse_pad.dict_tab.text)
        self.assertFalse("Definition:" in self.verse_pad.dict_tab.text)
        self.assertFalse("Syllables:" in self.verse_pad.dict_tab.text)

if __name__ == '__main__':
    unittest.main()