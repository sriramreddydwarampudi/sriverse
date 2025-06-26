from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty
import pronouncing
import enchant
import re
from functools import partial

class LyricVerse(BoxLayout):
    tempo_text = StringProperty("Tempo: Medium")
    time_sig_text = StringProperty("4/4 Time")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.dictionary = enchant.Dict("en_US")
        self.tempos = ['Slow', 'Medium', 'Fast']
        self.time_signatures = ['4/4', '3/4', '6/8']
        self.current_tempo = 1
        self.current_time_sig = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        # Toolbar
        toolbar = BoxLayout(size_hint=(1, 0.1))
        self.tempo_btn = Button(text=self.tempo_text)
        self.beat_btn = Button(text=self.time_sig_text)
        self.tempo_btn.bind(on_release=self.toggle_tempo)
        self.beat_btn.bind(on_release=self.toggle_time_signature)
        toolbar.add_widget(self.tempo_btn)
        toolbar.add_widget(self.beat_btn)
        self.add_widget(toolbar)
        
        # Text Input
        self.text_input = TextInput(
            size_hint=(1, 0.7),
            multiline=True,
            font_size=18,
            hint_text='Write your lyrics here...',
            background_color=(0.95, 0.95, 1, 1)
        )
        self.text_input.bind(text=self.on_text_change)
        self.add_widget(self.text_input)
        
        # Analysis Tabs
        self.tabs = AnalysisTabs()
        self.add_widget(self.tabs)
    
    def toggle_tempo(self, *args):
        self.current_tempo = (self.current_tempo + 1) % len(self.tempos)
        self.tempo_text = f"Tempo: {self.tempos[self.current_tempo]}"
    
    def toggle_time_signature(self, *args):
        self.current_time_sig = (self.current_time_sig + 1) % len(self.time_signatures)
        self.time_sig_text = f"{self.time_signatures[self.current_time_sig]} Time"
        self.update_analysis()
    
    def on_text_change(self, instance, text):
        Clock.schedule_once(partial(self.update_analysis), 0.1)
    
    def update_analysis(self, *args):
        text = self.text_input.text
        self.tabs.update_analyses(text, self.current_time_sig)

class AnalysisTabs(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 0.3)
        self.do_default_tab = False
        
        self.dict_tab = self.add_tab("Dictionary")
        self.rhyme_tab = self.add_tab("Rhymes")
        self.meter_tab = self.add_tab("Meter")
        self.beat_tab = self.add_tab("Rhythm")
        
        # Initialize with empty content
        for tab in [self.dict_tab, self.rhyme_tab, self.meter_tab, self.beat_tab]:
            tab.text = "Enter text to analyze..."

    def add_tab(self, name):
        scroll = ScrollView()
        content = Label(
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top',
            text_size=(None, None),
            padding=(10, 10)
        )
        content.bind(texture_size=content.setter('size'))
        scroll.add_widget(content)
        self.add_widget(scroll)
        return content

    def update_analyses(self, text, time_sig_index):
        if not text.strip():
            for tab in [self.dict_tab, self.rhyme_tab, self.meter_tab, self.beat_tab]:
                tab.text = "Enter text to analyze..."
            return
            
        self.update_dictionary(text)
        self.update_rhymes(text)
        self.update_meter(text)
        self.update_rhythm(text, time_sig_index)

    def clean_word(self, word):
        return re.sub(r'[^a-zA-Z]', '', word.lower())

    def update_dictionary(self, text):
        output = []
        words = set(self.clean_word(word) for word in text.split() if self.clean_word(word))
        
        for word in words:
            try:
                if not self.dict_tab.parent.parent.dictionary.check(word):
                    suggestions = self.dict_tab.parent.parent.dictionary.suggest(word)[:3]
                    output.append(f"[b]{word}[/b]\nSuggestions: {', '.join(suggestions)}\n")
            except:
                output.append(f"[b]{word}[/b]\n(Error checking word)\n")
        
        self.dict_tab.text = "\n".join(output) if output else "All words appear correct."

    def update_rhymes(self, text):
        words = [self.clean_word(w) for w in text.split() if self.clean_word(w)]
        if not words:
            self.rhyme_tab.text = "No words to analyze."
            return
            
        last_word = words[-1]
        try:
            rhymes = pronouncing.rhymes(last_word)[:10]
            phones = pronouncing.phones_for_word(last_word)
            
            output = [f"[b]Rhymes for '{last_word}':[/b]"]
            if rhymes:
                output.append(", ".join(rhymes))
            else:
                output.append("No perfect rhymes found.")
                
            if phones:
                output.append(f"\n\nPhonetics: {phones[0]}")
                
            self.rhyme_tab.text = "\n".join(output)
        except:
            self.rhyme_tab.text = "Error analyzing rhymes."

    def update_meter(self, text):
        pattern = []
        for word in [self.clean_word(w) for w in text.split() if self.clean_word(w)]:
            try:
                phones_list = pronouncing.phones_for_word(word)
                if phones_list:
                    stresses = pronouncing.stresses(phones_list[0])
                    pattern.extend([int(s) for s in stresses if s.isdigit()])
            except:
                continue
                
        if pattern:
            visual = ["¯" if s > 0 else "˘" for s in pattern]
            self.meter_tab.text = "Stress Pattern:\n" + " ".join(visual)
        else:
            self.meter_tab.text = "No stress pattern detected."

    def update_rhythm(self, text, time_sig_index):
        time_sigs = {
            0: ("4/4", "♩ ♩ ♩ ♩"),
            1: ("3/4", "♩ ♩ ♩"),
            2: ("6/8", "♪. ♪ ♪ ♪. ♪")
        }
        sig_name, beat_pattern = time_sigs.get(time_sig_index, ("4/4", "♩ ♩ ♩ ♩"))
        
        lines = text.split('\n')
        output = [
            f"[b]Time Signature: {sig_name}[/b]",
            f"Beat Pattern: {beat_pattern}",
            "",
            "[b]Syllables per line:[/b]"
        ]
        
        for i, line in enumerate(lines):
            if line.strip():
                count = 0
                for word in [self.clean_word(w) for w in line.split() if self.clean_word(w)]:
                    try:
                        phones = pronouncing.phones_for_word(word)
                        if phones:
                            count += len(pronouncing.syllable_count(phones[0]))
                    except:
                        continue
                output.append(f"Line {i+1}: {count} syllables")
        
        self.beat_tab.text = "\n".join(output)

class LyricVerseApp(App):
    def build(self):
        return LyricVerse()

if __name__ == "__main__":
    LyricVerseApp().run()
