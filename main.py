from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import pronouncing
import nltk
import enchant

nltk.download('punkt', quiet=True)
nltk.download('cmudict', quiet=True)
dictionary = enchant.Dict("en_US")

class VersePad(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Create toolbar for rhythm controls
        self.toolbar = BoxLayout(size_hint=(1, 0.1))
        self.tempo_btn = Button(text='Tempo: Medium')
        self.beat_btn = Button(text='4/4 Time')
        self.toolbar.add_widget(self.tempo_btn)
        self.toolbar.add_widget(self.beat_btn)
        self.add_widget(self.toolbar)
        
        # Main text area
        self.text_input = TextInput(
            size_hint=(1, 0.7), 
            multiline=True, 
            font_size=18,
            hint_text='Write your lyrics here...',
            background_color=(0.95, 0.95, 1, 1)  # Light blue background
        )
        self.add_widget(self.text_input)
        
        # Analysis tabs
        self.tabs = AnalysisTabs()
        self.add_widget(self.tabs)
        
        # Bind events
        self.text_input.bind(text=self.analyze_text)
        self.tempo_btn.bind(on_release=self.toggle_tempo)
        self.beat_btn.bind(on_release=self.toggle_time_signature)
        
        # Rhythm state
        self.tempo_index = 1  # Medium
        self.time_signature_index = 0  # 4/4

    def toggle_tempo(self, instance):
        tempos = ['Slow', 'Medium', 'Fast']
        self.tempo_index = (self.tempo_index + 1) % len(tempos)
        self.tempo_btn.text = f'Tempo: {tempos[self.tempo_index]}'

    def toggle_time_signature(self, instance):
        signatures = ['4/4', '3/4', '6/8']
        self.time_signature_index = (self.time_signature_index + 1) % len(signatures)
        self.beat_btn.text = f'{signatures[self.time_signature_index]} Time'

    def analyze_text(self, instance, text):
        self.tabs.update_analyses(text, self.time_signature_index)

class AnalysisTabs(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 0.3)
        self.do_default_tab = False
        
        # Create tabs
        self.dict_tab = self.add_tab("Dictionary")
        self.rhyme_tab = self.add_tab("Rhymes")
        self.meter_tab = self.add_tab("Meter")
        self.beat_tab = self.add_tab("Rhythm")

    def add_tab(self, name):
        tab = BoxLayout(orientation='vertical')
        scroll = ScrollView()
        content = Label(
            size_hint_y=None, 
            text="", 
            markup=True,
            halign='left',
            valign='top',
            text_size=(None, None)
        content.bind(texture_size=content.setter('size'))
        scroll.add_widget(content)
        tab.add_widget(scroll)
        self.add_widget(tab)
        return content

    def update_analyses(self, text, time_signature):
        self.update_dictionary(text)
        self.update_rhymes(text)
        self.update_meter(text)
        self.update_rhythm(text, time_signature)

    def update_dictionary(self, text):
        words = text.split()
        output = ""
        for word in words:
            if word.strip():
                cleaned_word = word.strip(",.!?;:'\"()[]{}")
                if cleaned_word:
                    suggestions = dictionary.suggest(cleaned_word)[:3]
                    output += f"[b]{word}[/b]\nSuggestions: {', '.join(suggestions)}\n\n"
        self.dict_tab.text = output or "No suggestions found."

    def update_rhymes(self, text):
        words = text.strip().split()
        output = ""
        if words:
            last_word = words[-1].strip(",.!?;:'\"()[]{}")
            if last_word:
                rhymes = pronouncing.rhymes(last_word)[:10]
                phones = pronouncing.phones_for_word(last_word)
                output = f"[b]Rhymes for '{last_word}':[/b]\n{', '.join(rhymes)}"
                output += f"\n\nPhonetics: {phones[0] if phones else 'N/A'}"
        self.rhyme_tab.text = output or "No rhymes found."

    def update_meter(self, text):
        pattern = []
        for word in text.split():
            cleaned_word = word.strip(",.!?;:'\"()[]{}")
            if cleaned_word:
                phones_list = pronouncing.phones_for_word(cleaned_word)
                if phones_list:
                    stresses = pronouncing.stresses(phones_list[0])
                    pattern.extend([int(s) for s in stresses if s.isdigit()])
        
        # Visual representation
        visual_pattern = []
        for stress in pattern:
            if stress == 0:
                visual_pattern.append("˘")  # breve for unstressed
            else:
                visual_pattern.append("¯")  # macron for stressed
        
        self.meter_tab.text = "Stress Pattern:\n" + ' '.join(visual_pattern) if visual_pattern else "No stress pattern detected."

    def update_rhythm(self, text, time_signature):
        signatures = {
            0: ("4/4", "♩ ♩ ♩ ♩"),
            1: ("3/4", "♩ ♩ ♩"),
            2: ("6/8", "♪. ♪ ♪ ♪. ♪")
        }
        sig_name, beat_pattern = signatures.get(time_signature, ("4/4", "♩ ♩ ♩ ♩"))
        
        # Count syllables per line
        lines = text.split('\n')
        output = f"[b]Time Signature: {sig_name}[/b]\nBeat Pattern: {beat_pattern}\n\n"
        output += "[b]Syllables per line:[/b]\n"
        
        for i, line in enumerate(lines):
            if line.strip():
                words = line.split()
                syllable_count = 0
                for word in words:
                    cleaned_word = word.strip(",.!?;:'\"()[]{}")
                    if cleaned_word:
                        phones_list = pronouncing.phones_for_word(cleaned_word)
                        if phones_list:
                            syllable_count += len(pronouncing.syllable_count(phones_list[0]))
                output += f"Line {i+1}: {syllable_count} syllables\n"
        
        self.beat_tab.text = output

class VersePadApp(App):
    def build(self):
        return VersePad()

if __name__ == "__main__":
    VersePadApp().run()
