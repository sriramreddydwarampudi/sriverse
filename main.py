from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import pronouncing
import nltk
import re
import random
from collections import defaultdict
import difflib

# Initialize components
try:
    nltk.download('punkt', quiet=True)
    nltk.download('cmudict', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('words', quiet=True)
    from nltk.corpus import wordnet, words
    english_words = set(words.words())
except:
    wordnet = None
    english_words = set()

class VersePad(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light gray background
        
        # Text input (top 65% of screen)
        self.text_input = TextInput(
            size_hint=(1, 0.65),
            font_size=16,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            hint_text="Write your poem here...",
            multiline=True
        )
        self.add_widget(self.text_input)
        
        # Analysis tabs (bottom 35% of screen)
        self.tabs = TabbedPanel(
            size_hint=(1, 0.35),
            do_default_tab=False,
            tab_width=100
        )
        
        # Create tabs
        self.create_tab("Dictionary", "dict_tab")
        self.create_tab("Rhymes", "rhyme_tab")
        self.create_tab("Advanced", "advanced_tab")
        self.create_tab("Meter", "meter_tab")
        self.create_tab("Grammar", "grammar_tab")
        
        self.add_widget(self.tabs)
        self.text_input.bind(text=self.on_text_change)
        
        # Musical note mapping for rhythm
        self.note_map = {
            0: "♪",    # unstressed = eighth note
            1: "♩",    # stressed = quarter note
            2: "♫"     # very stressed = beamed eighth notes
        }
    
    def create_tab(self, name, attr_name):
        """Helper to create consistent tabs"""
        scroll = ScrollView()
        label = Label(
            size_hint_y=None,
            markup=True,
            padding=(10, 10),
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        label.bind(texture_size=label.setter('size'))
        scroll.add_widget(label)
        
        tab = TabbedPanelItem(text=name)
        tab.add_widget(scroll)
        self.tabs.add_widget(tab)
        setattr(self, attr_name, label)
    
    def on_text_change(self, instance, value):
        self.update_analyses(value)
    
    def update_analyses(self, text):
        self.update_dictionary(text)
        self.update_rhymes(text)
        self.update_advanced_features(text)
        self.update_meter(text)
        self.update_grammar(text)
    
    def get_word_definition(self, word):
        """Get definition using WordNet"""
        if wordnet is None:
            return "WordNet not available"
        
        try:
            synsets = wordnet.synsets(word.lower())
            if synsets:
                # Get the most common definition
                definition = synsets[0].definition()
                return definition.capitalize()
            else:
                return "No definition found"
        except:
            return "Error getting definition"
    
    def get_syllable_division(self, word):
        """Get syllable division from phonemes"""
        try:
            phones = pronouncing.phones_for_word(word)
            if phones:
                # Convert phonemes to syllables
                syllable_count = pronouncing.syllable_count(phones[0])
                if syllable_count <= 1:
                    return word
                
                # Use CMU dict for syllable breaks
                phones_list = phones[0].split()
                syllables = []
                current = []
                
                for phone in phones_list:
                    current.append(phone)
                    # Syllable boundaries based on vowel sounds
                    if any(char in phone for char in '012'):
                        syllables.append(''.join(current))
                        current = []
                
                # Handle any remaining consonants
                if current:
                    if syllables:
                        syllables[-1] += ''.join(current)
                    else:
                        syllables.append(''.join(current))
                
                # Create hyphenated representation
                return '-'.join(syllables)
            return word
        except:
            return word
    
    def is_word_spelled_correctly(self, word):
        """Check spelling using NLTK words corpus"""
        return word.lower() in english_words
    
    def get_spelling_suggestions(self, word):
        """Get spelling suggestions using similarity matching"""
        if not english_words:
            return []
        
        word = word.lower()
        # Find similar words in the dictionary
        similar_words = difflib.get_close_matches(word, english_words, n=3, cutoff=0.7)
        return similar_words
    
    def update_dictionary(self, text):
        words = [w.strip('.,!?;:"()[]') for w in text.split() if w.strip()][-5:]  # Last 5 words
        output = ""
        
        for word in words:
            clean_word = re.sub(r'[^a-zA-Z]', '', word)
            if clean_word:
                output += f"\n[b][color=3333ff]{word}:[/color][/b]"
                
                # Check spelling
                if self.is_word_spelled_correctly(clean_word):
                    output += " ✓ (correct spelling)"
                else:
                    suggestions = self.get_spelling_suggestions(clean_word)
                    if suggestions:
                        output += f"\n  [color=ff6600]Suggestions: {', '.join(suggestions)}[/color]"
                    else:
                        output += f"\n  [color=ff6600]Possible misspelling[/color]"
                
                # Get definition
                definition = self.get_word_definition(clean_word)
                output += f"\n  [color=666666][i]Definition:[/i][/color] {definition}\n"
        
        self.dict_tab.text = output or "No words to analyze"
    
    def update_rhymes(self, text):
        words = [w.strip('.,!?;:"()[]') for w in text.split() if w.strip()]
        last_word = words[-1] if words else ""
        last_word = re.sub(r'[^a-zA-Z]', '', last_word)
        output = ""
        
        if last_word:
            try:
                rhymes = pronouncing.rhymes(last_word)[:15]
                phones = pronouncing.phones_for_word(last_word)
                
                output += f"[b][color=ff3333]Rhymes for '{last_word}':[/color][/b]\n"
                
                # Add syllable division for the original word
                syllable_div = self.get_syllable_division(last_word)
                output += f"[color=666666]Syllables: {syllable_div}[/color]\n\n"
                
                if rhymes:
                    output += "[b]Perfect rhymes:[/b]\n"
                    for rhyme in rhymes:
                        rhyme_syllables = self.get_syllable_division(rhyme)
                        output += f"• {rhyme} ({rhyme_syllables})\n"
                else:
                    output += "No perfect rhymes found"
                
                # Add phonetic information
                if phones:
                    output += f"\n[b]Phonetics:[/b] /{phones[0]}/"
                    
            except Exception as e:
                output = f"Rhyme analysis failed: {str(e)}"
        else:
            output = "No text to analyze"
        
        self.rhyme_tab.text = output
    
    def update_advanced_features(self, text):
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        output = "[b][color=9933cc]Advanced Poetic Features:[/color][/b]\n\n"
        
        if not lines:
            self.advanced_tab.text = output + "No text to analyze"
            return
        
        # Internal rhymes
        internal_output = self.find_internal_rhymes(lines[-1] if lines else "")
        output += internal_output + "\n"
        
        # Multi-syllabic rhyme suggestions
        if lines:
            last_line = lines[-1]
            if last_line.split():
                last_word = last_line.split()[-1]
                last_word = re.sub(r'[^a-zA-Z]', '', last_word)
                if last_word:
                    multi_output = self.generate_multi_syllabic_rhymes(last_word)
                    output += multi_output
                else:
                    output += "No word for multi-syllabic rhymes"
            else:
                output += "No word for multi-syllabic rhymes"
        else:
            output += "No text for multi-syllabic rhymes"
        
        self.advanced_tab.text = output
    
    def find_internal_rhymes(self, line):
        """Find internal rhymes within a line"""
        if not line:
            return "No line to analyze for internal rhymes"
        
        words = [re.sub(r'[^a-zA-Z]', '', w.lower()) for w in line.split()]
        words = [w for w in words if w and len(w) > 2]  # Only consider words >2 letters
        
        rhyme_pairs = []
        rhyme_groups = defaultdict(list)
        
        # For each word, find words later in the line that rhyme with it
        for i, word in enumerate(words):
            rhymes = set(pronouncing.rhymes(word))
            for j in range(i+1, len(words)):
                if words[j] in rhymes and words[j] != word:
                    rhyme_pairs.append((word, words[j]))
                    rhyme_groups[word].append(words[j])
        
        output = "[b]Internal Rhymes:[/b]\n"
        if not rhyme_pairs:
            output += "No internal rhymes detected\n"
            return output
        
        # Group rhymes
        for word, rhymes in rhyme_groups.items():
            output += f"• '{word}' rhymes with: {', '.join(rhymes)}\n"
        
        output += "\n[color=666666]Internal rhymes occur when words within the same line sound similar[/color]"
        return output
    
    def generate_multi_syllabic_rhymes(self, word):
        """Generate multi-syllabic rhyme suggestions"""
        try:
            syllable_div = self.get_syllable_division(word)
            syllables = syllable_div.split('-')
            
            output = f"[b]Multi-syllabic Rhymes for '{word}':[/b]\n"
            output += f"Syllables: {syllable_div}\n\n"
            
            # Find rhymes for the last syllable
            last_syllable = syllables[-1]
            last_syllable_rhymes = set()
            
            # Get words that rhyme with the target word
            all_rhymes = pronouncing.rhymes(word)
            
            # Find multi-syllabic rhymes (words with same ending syllables)
            multi_syllabic_rhymes = []
            for rhyme in all_rhymes:
                # Skip single-syllable rhymes
                if pronouncing.syllable_count(pronouncing.phones_for_word(rhyme)[0]) > 1:
                    multi_syllabic_rhymes.append(rhyme)
            
            # Limit to 10 results
            multi_syllabic_rhymes = multi_syllabic_rhymes[:10]
            
            if multi_syllabic_rhymes:
                output += f"[b]Multi-syllabic rhymes:[/b]\n"
                for rhyme in multi_syllabic_rhymes:
                    rhyme_syllables = self.get_syllable_division(rhyme)
                    output += f"• {rhyme} ({rhyme_syllables})\n"
                
                # Generate phrase suggestions using the rhymes
                output += "\n[b]Phrase Suggestions:[/b]\n"
                if multi_syllabic_rhymes:
                    rhyme_word = random.choice(multi_syllabic_rhymes)
                    output += f"Try: [i]'{word}'[/i] with [i]'{rhyme_word}'[/i]\n"
                    output += f"Example: [color=666666]\"The {word} in the {rhyme_word}\"[/color]\n\n"
                    
                    # Create a simple phrase pattern
                    subjects = ["the", "my", "your", "our", "that"]
                    verbs = ["shines", "glows", "flows", "grows", "shows"]
                    rhyme_word2 = random.choice(multi_syllabic_rhymes) if len(multi_syllabic_rhymes) > 1 else rhyme_word
                    output += f"Pattern: [color=3333ff][i]{random.choice(subjects)} {word} {random.choice(verbs)} like {rhyme_word2}[/i][/color]"
            else:
                output += "No multi-syllabic rhymes found\n"
            
            output += "\n[color=666666]Multi-syllabic rhymes match the ending sounds across multiple syllables[/color]"
            return output
        except Exception as e:
            return f"Multi-syllabic rhyme generation failed: {str(e)}"
    
    def update_meter(self, text):
        lines = [line.strip() for line in text.split('\n') if line.strip()][-3:]  # Last 3 lines
        output = ""
        
        if lines:
            try:
                output += "[b][color=9933cc]Rhythm & Musical Notes:[/color][/b]\n\n"
                
                for line_num, line in enumerate(lines, 1):
                    words = [w.strip('.,!?;:"()[]') for w in line.split() if w.strip()]
                    clean_words = [re.sub(r'[^a-zA-Z]', '', w) for w in words if re.sub(r'[^a-zA-Z]', '', w)]
                    
                    if clean_words:
                        output += f"[b]Line {line_num}:[/b] {line}\n"
                        
                        # Get stress pattern
                        stress_pattern = []
                        syllable_pattern = []
                        
                        for word in clean_words:
                            phones = pronouncing.phones_for_word(word)
                            if phones:
                                stresses = pronouncing.stresses(phones[0])
                                word_stresses = [int(s) for s in stresses if s.isdigit()]
                                stress_pattern.extend(word_stresses)
                                
                                # Add syllable info
                                syllable_div = self.get_syllable_division(word)
                                syllable_pattern.append(syllable_div)
                        
                        # Display stress pattern with numbers
                        if stress_pattern:
                            output += f"Stress: {' '.join(map(str, stress_pattern))}\n"
                            
                            # Convert to musical notes
                            notes = [self.note_map.get(stress, "♪") for stress in stress_pattern]
                            output += f"Notes: {' '.join(notes)}\n"
                            
                            # Add rhythm analysis
                            rhythm_type = self.analyze_rhythm(stress_pattern)
                            output += f"[color=666666]Rhythm: {rhythm_type}[/color]\n"
                        
                        # Show syllable breakdown
                        if syllable_pattern:
                            output += f"Syllables: {' | '.join(syllable_pattern)}\n"
                        
                        output += "\n"
                
                # Overall rhythm summary
                if lines:
                    output += self.get_rhythm_summary(lines)
                        
            except Exception as e:
                output = f"Meter analysis failed: {str(e)}"
        else:
            output = "No text to analyze"
        
        self.meter_tab.text = output
    
    def analyze_rhythm(self, pattern):
        """Analyze the rhythm pattern and categorize it"""
        if not pattern:
            return "No pattern"
        
        # Convert pattern to string for easier analysis
        pattern_str = ''.join(map(str, pattern))
        
        # Common poetic meters
        if '01' * (len(pattern) // 2) == pattern_str[:len('01' * (len(pattern) // 2))]:
            return "Iambic (unstressed-stressed)"
        elif '10' * (len(pattern) // 2) == pattern_str[:len('10' * (len(pattern) // 2))]:
            return "Trochaic (stressed-unstressed)"
        elif '001' in pattern_str or '100' in pattern_str:
            return "Anapestic/Dactylic (triple meter)"
        elif pattern.count(1) > pattern.count(0):
            return "Stress-heavy"
        elif pattern.count(0) > pattern.count(1):
            return "Light stress"
        else:
            return "Mixed rhythm"
    
    def get_rhythm_summary(self, lines):
        """Get overall rhythm summary for multiple lines"""
        total_syllables = 0
        total_stresses = 0
        
        for line in lines:
            words = [re.sub(r'[^a-zA-Z]', '', w) for w in line.split() if re.sub(r'[^a-zA-Z]', '', w)]
            for word in words:
                try:
                    phones = pronouncing.phones_for_word(word)
                    if phones:
                        stresses = pronouncing.stresses(phones[0])
                        syllable_count = len([s for s in stresses if s.isdigit()])
                        stress_count = len([s for s in stresses if s == '1'])
                        total_syllables += syllable_count
                        total_stresses += stress_count
                except:
                    continue
        
        if total_syllables > 0:
            stress_ratio = total_stresses / total_syllables
            output = "[b]Overall Analysis:[/b]\n"
            output += f"Total syllables: {total_syllables}\n"
            output += f"Stressed syllables: {total_stresses}\n"
            output += f"Stress ratio: {stress_ratio:.2f}\n"
            
            if stress_ratio > 0.6:
                output += "Style: Heavy, dramatic\n"
            elif stress_ratio > 0.4:
                output += "Style: Balanced rhythm\n"
            else:
                output += "Style: Light, flowing\n"
                
            # Suggest musical tempo
            if total_syllables > 30:
                output += "Suggested tempo: Allegro (fast) ♩=120-168\n"
            elif total_syllables > 15:
                output += "Suggested tempo: Moderato (moderate) ♩=108-120\n"
            else:
                output += "Suggested tempo: Andante (slow) ♩=76-108\n"
                
            return output
        
        return ""
    
    def update_grammar(self, text):
        if not text.strip():
            self.grammar_tab.text = "No text to analyze"
            return
            
        # Enhanced grammar checks
        issues = []
        suggestions = []
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        for i, sent in enumerate(sentences[:5]):  # Check first 5 sentences
            words = sent.split()
            if words:
                # Capitalization check
                if words[0] and words[0][0].islower():
                    issues.append(f"Line {i+1}: First word not capitalized")
                
                # Length check
                if len(words) > 20:
                    issues.append(f"Line {i+1}: Very long ({len(words)} words)")
                elif len(words) == 1:
                    suggestions.append(f"Line {i+1}: Very short - consider expanding")
                
                # Repetition check
                word_freq = {}
                for word in words:
                    clean = word.lower().strip('.,!?;:"()[]')
                    word_freq[clean] = word_freq.get(clean, 0) + 1
                
                repeated = [w for w, c in word_freq.items() if c > 2 and len(w) > 3]
                if repeated:
                    suggestions.append(f"Line {i+1}: Repeated words: {', '.join(repeated)}")
        
        # Punctuation check
        if text.strip() and not text.rstrip()[-1] in {'.', '!', '?', ':', ';'}:
            issues.append("Missing ending punctuation")
        
        # Poetry-specific suggestions
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if len(lines) > 1:
            line_lengths = [len(line.split()) for line in lines]
            avg_length = sum(line_lengths) / len(line_lengths)
            
            if max(line_lengths) - min(line_lengths) > 5:
                suggestions.append("Consider more consistent line lengths for better flow")
            
            if avg_length > 12:
                suggestions.append("Long lines - consider breaking for better rhythm")
        
        # Format output
        output = ""
        if issues:
            output += "[b][color=ff3333]Issues:[/color][/b]\n• " + "\n• ".join(issues) + "\n\n"
        
        if suggestions:
            output += "[b][color=ff9900]Suggestions:[/color][/b]\n• " + "\n• ".join(suggestions) + "\n\n"
        
        if not issues and not suggestions:
            output = "[color=33cc33]✓ No obvious issues found![/color]\n\n"
        
        # Add word count and reading stats
        word_count = len([w for w in text.split() if w.strip()])
        line_count = len([line for line in text.split('\n') if line.strip()])
        
        output += f"[b]Statistics:[/b]\n"
        output += f"Words: {word_count}\n"
        output += f"Lines: {line_count}\n"
        if word_count > 0:
            output += f"Avg words/line: {word_count/max(line_count, 1):.1f}\n"
        
        self.grammar_tab.text = output

class VersePadApp(App):
    def build(self):
        self.title = "VersePad - Enhanced Poetry Assistant"
        return VersePad()

if __name__ == "__main__":
    VersePadApp().run()
