from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.utils import platform
import pronouncing
import nltk
import enchant
import os
import json
import re
from datetime import datetime

# Initialize components
try:
    nltk.download('punkt', quiet=True)
    nltk.download('cmudict', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    from nltk.corpus import wordnet
    dictionary = enchant.Dict("en_US")
except:
    dictionary = None
    wordnet = None

class VersePad(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light gray background
        
        # Text input (top 70% of screen)
        self.text_input = TextInput(
            size_hint=(1, 0.7),
            font_size=16,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            hint_text="Write your poem here...",
            multiline=True
        )
                
        self.add_widget(self.text_input)
        self.add_widget(self.export_btn)
        
        # Analysis tabs (bottom 25% of screen)
        self.tabs = TabbedPanel(
            size_hint=(1, 0.25),
            do_default_tab=False,
            tab_width=100
        )
        
        # Create tabs
        self.create_tab("Dictionary", "dict_tab")
        self.create_tab("Rhymes", "rhyme_tab")
        self.create_tab("Meter", "meter_tab")
        self.create_tab("Grammar", "grammar_tab")
        
        self.add_widget(self.tabs)
        self.text_input.bind(text=self.on_text_change)
    
    def get_export_path(self):
        """Get appropriate export path based on platform"""
        if platform == 'android':
            from android.storage import primary_external_storage_path
            return os.path.join(primary_external_storage_path(), 'VersePad')
        else:
            # Desktop/other platforms
            return os.path.expanduser("~/VersePad")
    
    def export_to_txt(self, instance):
        """Export poem and analysis to text file"""
        try:
            # Create export directory
            export_dir = self.get_export_path()
            os.makedirs(export_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"poem_{timestamp}.txt"
            filepath = os.path.join(export_dir, filename)
            
            # Get current text and analysis
            poem_text = self.text_input.text
            
            # Generate export content
            export_content = self.generate_export_content(poem_text)
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(export_content)
            
            # Show success message (simplified for cross-platform)
            print(f"Exported to: {filepath}")
            
        except Exception as e:
            print(f"Export failed: {str(e)}")
    
    def generate_export_content(self, text):
        """Generate formatted content for export"""
        content = []
        content.append("=" * 50)
        content.append("VERSEPAD POETRY EXPORT")
        content.append("=" * 50)
        content.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")
        
        # Original poem
        content.append("POEM:")
        content.append("-" * 20)
        content.append(text if text.strip() else "No poem text")
        content.append("")
        
        if text.strip():
            # Dictionary analysis
            content.append("DICTIONARY ANALYSIS:")
            content.append("-" * 20)
            content.extend(self.export_dictionary_analysis(text))
            content.append("")
            
            # Rhyme analysis
            content.append("RHYME ANALYSIS:")
            content.append("-" * 20)
            content.extend(self.export_rhyme_analysis(text))
            content.append("")
            
            # Rhythm analysis
            content.append("RHYTHM ANALYSIS:")
            content.append("-" * 20)
            content.extend(self.export_rhythm_analysis(text))
            content.append("")
            
            # Statistics
            content.append("STATISTICS:")
            content.append("-" * 20)
            content.extend(self.export_statistics(text))
        
        return "\n".join(content)
    
    def export_dictionary_analysis(self, text):
        """Export dictionary analysis in plain text"""
        words = [w.strip('.,!?;:"()[]') for w in text.split() if w.strip()][-5:]
        lines = []
        
        for word in words:
            clean_word = re.sub(r'[^a-zA-Z]', '', word)
            if clean_word:
                lines.append(f"{word}:")
                
                # Check spelling
                if dictionary:
                    try:
                        if dictionary.check(clean_word):
                            lines.append("  Spelling: Correct")
                        else:
                            suggestions = dictionary.suggest(clean_word)
                            if suggestions:
                                lines.append(f"  Suggestions: {', '.join(suggestions[:3])}")
                    except:
                        lines.append("  Spelling: Error checking")
                
                # Get definition
                definition = self.get_word_definition(clean_word)
                lines.append(f"  Definition: {definition}")
                lines.append("")
        
        return lines if lines else ["No words to analyze"]
    
    def export_rhyme_analysis(self, text):
        """Export rhyme analysis in plain text"""
        words = [w.strip('.,!?;:"()[]') for w in text.split() if w.strip()]
        last_word = words[-1] if words else ""
        last_word = re.sub(r'[^a-zA-Z]', '', last_word)
        lines = []
        
        if last_word:
            try:
                rhymes = pronouncing.rhymes(last_word)[:15]
                phones = pronouncing.phones_for_word(last_word)
                
                lines.append(f"Rhymes for '{last_word}':")
                
                # Add syllable division for the original word
                syllable_div = self.get_syllable_division(last_word)
                lines.append(f"Syllables: {syllable_div}")
                lines.append("")
                
                if rhymes:
                    lines.append("Rhyming words with syllables:")
                    for rhyme in rhymes:
                        rhyme_syllables = self.get_syllable_division(rhyme)
                        lines.append(f"  {rhyme} ({rhyme_syllables})")
                else:
                    lines.append("No rhymes found")
                
                # Add phonetic information
                if phones:
                    lines.append(f"Phonetics: /{phones[0]}/")
                    
            except Exception as e:
                lines.append(f"Rhyme analysis failed: {str(e)}")
        else:
            lines.append("No text to analyze")
        
        return lines
    
    def export_rhythm_analysis(self, text):
        """Export rhythm analysis in plain text"""
        lines = [line.strip() for line in text.split('\n') if line.strip()][-3:]
        export_lines = []
        
        if lines:
            try:
                for line_num, line in enumerate(lines, 1):
                    words = [w.strip('.,!?;:"()[]') for w in line.split() if w.strip()]
                    clean_words = [re.sub(r'[^a-zA-Z]', '', w) for w in words if re.sub(r'[^a-zA-Z]', '', w)]
                    
                    if clean_words:
                        export_lines.append(f"Line {line_num}: {line}")
                        
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
                        
                        # Display stress pattern
                        if stress_pattern:
                            export_lines.append(f"  Stress: {' '.join(map(str, stress_pattern))}")
                            
                            # Convert to rhythm symbols
                            symbols = [self.rhythm_symbols.get(stress, "-") for stress in stress_pattern]
                            export_lines.append(f"  Rhythm: {' '.join(symbols)}")
                            
                            # Add rhythm analysis
                            rhythm_type = self.analyze_rhythm(stress_pattern)
                            export_lines.append(f"  Type: {rhythm_type}")
                        
                        # Show syllable breakdown
                        if syllable_pattern:
                            export_lines.append(f"  Syllables: {' | '.join(syllable_pattern)}")
                        
                        export_lines.append("")
                
                # Overall rhythm summary
                if lines:
                    summary = self.get_rhythm_summary_text(lines)
                    export_lines.extend(summary)
                        
            except Exception as e:
                export_lines.append(f"Rhythm analysis failed: {str(e)}")
        else:
            export_lines.append("No text to analyze")
        
        return export_lines
    
    def export_statistics(self, text):
        """Export statistics in plain text"""
        word_count = len([w for w in text.split() if w.strip()])
        line_count = len([line for line in text.split('\n') if line.strip()])
        
        lines = [
            f"Words: {word_count}",
            f"Lines: {line_count}"
        ]
        
        if word_count > 0:
            lines.append(f"Average words per line: {word_count/max(line_count, 1):.1f}")
        
        return lines
    
    def get_rhythm_summary_text(self, lines):
        """Get rhythm summary for export"""
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
        
        summary = ["Overall Analysis:"]
        if total_syllables > 0:
            stress_ratio = total_stresses / total_syllables
            summary.extend([
                f"Total syllables: {total_syllables}",
                f"Stressed syllables: {total_stresses}",
                f"Stress ratio: {stress_ratio:.2f}"
            ])
            
            if stress_ratio > 0.6:
                summary.append("Style: Heavy, dramatic")
            elif stress_ratio > 0.4:
                summary.append("Style: Balanced rhythm")
            else:
                summary.append("Style: Light, flowing")
                
            # Suggest musical tempo
            if total_syllables > 30:
                summary.append("Suggested tempo: Allegro (fast) 120-168 BPM")
            elif total_syllables > 15:
                summary.append("Suggested tempo: Moderato (moderate) 108-120 BPM")
            else:
                summary.append("Suggested tempo: Andante (slow) 76-108 BPM")
        
        return summary
        
        # Musical note mapping for rhythm (using ASCII-safe alternatives)
        self.note_map = {
            0: "u",     # unstressed = u
            1: "S",     # stressed = S (capital)
            2: "SS"     # very stressed = SS
        }
        
        # Alternative visual rhythm symbols
        self.rhythm_symbols = {
            0: "-",     # unstressed = dash
            1: "/",     # stressed = slash
            2: "^"      # very stressed = caret
        }
        
        # Create export button
        self.export_btn = Button(
            text="Export to TXT",
            size_hint=(1, 0.05),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        self.export_btn.bind(on_press=self.export_to_txt)
    
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
                # Convert phonemes to syllables (simplified approach)
                phoneme_list = phones[0].split()
                syllables = []
                current_syllable = []
                
                for phoneme in phoneme_list:
                    current_syllable.append(phoneme)
                    # If phoneme contains a vowel sound (0, 1, or 2), it's a syllable nucleus
                    if any(char in phoneme for char in '012'):
                        syllables.append(''.join(current_syllable))
                        current_syllable = []
                
                # Add any remaining phonemes to the last syllable
                if current_syllable and syllables:
                    syllables[-1] += ''.join(current_syllable)
                elif current_syllable:
                    syllables.append(''.join(current_syllable))
                
                # Convert back to approximate syllables
                syllable_count = len([s for s in syllables if any(c in s for c in '012')])
                if syllable_count <= 1:
                    return word
                else:
                    # Simple syllable division approximation
                    return self.divide_syllables_simple(word, syllable_count)
            return word
        except:
            return word
    
    def divide_syllables_simple(self, word, syllable_count):
        """Simple syllable division based on common patterns"""
        if syllable_count <= 1:
            return word
        
        # Very basic syllable division rules
        vowels = 'aeiouAEIOU'
        syllables = []
        current = ""
        vowel_count = 0
        
        for i, char in enumerate(word):
            current += char
            if char in vowels:
                vowel_count += 1
                # If we have enough vowels and there's more text, try to split
                if vowel_count > 1 and i < len(word) - 1:
                    # Look for consonant clusters to split on
                    if i + 1 < len(word) and word[i + 1] not in vowels:
                        # Find a good place to split
                        split_point = len(current) - 1
                        syllables.append(current[:split_point])
                        current = current[split_point:]
                        vowel_count = 1
        
        if current:
            syllables.append(current)
        
        return "-".join(syllables) if len(syllables) > 1 else word
    
    def update_dictionary(self, text):
        if dictionary is None:
            self.dict_tab.text = "Dictionary unavailable"
            return
            
        words = [w.strip('.,!?;:"()[]') for w in text.split() if w.strip()][-5:]  # Last 5 words
        output = ""
        
        for word in words:
            clean_word = re.sub(r'[^a-zA-Z]', '', word)
            if clean_word:
                output += f"\n[b][color=3333ff]{word}:[/color][/b]"
                
                # Check spelling
                try:
                    if dictionary.check(clean_word):
                        output += " ✓ (correct spelling)"
                    else:
                        suggestions = dictionary.suggest(clean_word)
                        if suggestions:
                            output += f"\n  [color=ff6600]Suggestions: {', '.join(suggestions[:3])}[/color]"
                except:
                    output += "\n  Error checking spelling"
                
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
                    output += "[b]Rhyming words with syllables:[/b]\n"
                    for rhyme in rhymes:
                        rhyme_syllables = self.get_syllable_division(rhyme)
                        output += f"• {rhyme} ({rhyme_syllables})\n"
                else:
                    output += "No rhymes found"
                
                # Add phonetic information
                if phones:
                    output += f"\n[b]Phonetics:[/b] /{phones[0]}/"
                    
            except Exception as e:
                output = f"Rhyme analysis failed: {str(e)}"
        else:
            output = "No text to analyze"
        
        self.rhyme_tab.text = output
    
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
                            
                            # Convert to musical notes (ASCII-safe)
                            notes = [self.note_map.get(stress, "u") for stress in stress_pattern]
                            symbols = [self.rhythm_symbols.get(stress, "-") for stress in stress_pattern]
                            output += f"Notes: {' '.join(notes)}\n"
                            output += f"Visual: {' '.join(symbols)}\n"
                            
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
                output += "Suggested tempo: Allegro (fast) 120-168 BPM\n"
            elif total_syllables > 15:
                output += "Suggested tempo: Moderato (moderate) 108-120 BPM\n"
            else:
                output += "Suggested tempo: Andante (slow) 76-108 BPM\n"
                
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
