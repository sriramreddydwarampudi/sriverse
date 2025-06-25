from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import pronouncing
import nltk
import enchant
from language_tool_python import LanguageTool
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Initialize components
nltk.download('punkt', quiet=True)
nltk.download('cmudict', quiet=True)
dictionary = enchant.Dict("en_US")
grammar_tool = LanguageTool('en-US')

class VersePad(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Text input area
        self.text_input = TextInput(
            size_hint=(1, 0.7),
            multiline=True,
            font_size=18
        )
        self.add_widget(self.text_input)
        
        # Analysis tabs
        self.tabs = AnalysisTabs()
        self.add_widget(self.tabs)

    def analyze_text(self):
        text = self.text_input.text
        self.tabs.update_analyses(text)

class AnalysisTabs(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 0.3)
        self.do_default_tab = False
        
        # Create tabs
        self.dict_tab = self.add_tab("Dictionary")
        self.rhyme_tab = self.add_tab("Rhymes")
        self.meter_tab = self.add_tab("Meter")
        self.grammar_tab = self.add_tab("Grammar")
    
    def add_tab(self, name):
        tab = BoxLayout(orientation='vertical')
        scroll = ScrollView()
        content = Label(size_hint_y=None)
        content.bind(texture_size=content.setter('size'))
        scroll.add_widget(content)
        tab.add_widget(scroll)
        self.add_widget(tab)
        return content
    
    def update_analyses(self, text):
        self.update_dictionary(text)
        self.update_rhymes(text)
        self.update_meter(text)
        self.update_grammar(text)
    
    def update_dictionary(self, text):
        words = text.split()
        output = ""
        for word in words:
            if word.strip():
                output += f"\n[color=3333ff]{word}:[/color] "
                # Get definitions
                suggestions = dictionary.suggest(word)
                output += f"\n  Suggestions: {', '.join(suggestions[:3])}"
        self.dict_tab.text = output
    
    def update_rhymes(self, text):
        last_word = text.strip().split()[-1] if text.strip() else ""
        output = ""
        if last_word:
            rhymes = pronouncing.rhymes(last_word)[:10]
            phones = pronouncing.phones_for_word(last_word)
            output += f"\n[color=ff3333]Rhymes for '{last_word}':[/color]"
            output += f"\n{', '.join(rhymes)}"
            output += f"\n\nPhonetics: {phones[0] if phones else 'N/A'}"
        self.rhyme_tab.text = output
    
    def update_meter(self, text):
        # Generate stress pattern visualization
        buf = BytesIO()
        stress_pattern = self.get_stress_pattern(text)
        plt.figure(figsize=(4, 1))
        plt.bar(range(len(stress_pattern)), stress_pattern, color='skyblue')
        plt.ylim(0, 1)
        plt.axis('off')
        plt.savefig(buf, format='png')
        plt.close()
        img_data = base64.b64encode(buf.getvalue()).decode()
        
        # Meter analysis text
        analysis = f"Stress pattern: {' '.join(map(str, stress_pattern))}"
        self.meter_tab.text = f"{analysis}\n[img=data:image/png;base64,{img_data}]"
    
    def get_stress_pattern(self, text):
        pattern = []
        for word in text.split():
            phones_list = pronouncing.phones_for_word(word)
            if phones_list:
                stresses = pronouncing.stresses(phones_list[0])
                pattern.extend([int(s) for s in stresses if s.isdigit()])
        return pattern or [0]
    
    def update_grammar(self, text):
        matches = grammar_tool.check(text)
        output = ""
        for match in matches[:5]:  # Show top 5 errors
            output += f"\n• {match.message} [color=ff0000]({match.context})[/color]"
        self.grammar_tab.text = output or "No grammar errors found"

class VersePadApp(App):
    def build(self):
        return VersePad()

if __name__ == "__main__":
    VersePadApp().run()
