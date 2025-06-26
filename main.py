from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
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
        self.text_input = TextInput(size_hint=(1, 0.7), multiline=True, font_size=18)
        self.add_widget(self.text_input)
        self.tabs = AnalysisTabs()
        self.add_widget(self.tabs)
        self.text_input.bind(text=lambda *a: self.analyze_text())

    def analyze_text(self):
        self.tabs.update_analyses(self.text_input.text)

class AnalysisTabs(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 0.3)
        self.do_default_tab = False
        self.dict_tab = self.add_tab("Dictionary")
        self.rhyme_tab = self.add_tab("Rhymes")
        self.meter_tab = self.add_tab("Meter")

    def add_tab(self, name):
        tab = BoxLayout(orientation='vertical')
        scroll = ScrollView()
        content = Label(size_hint_y=None, text="", markup=True)
        content.bind(texture_size=content.setter('size'))
        scroll.add_widget(content)
        tab.add_widget(scroll)
        self.add_widget(tab)
        return content

    def update_analyses(self, text):
        self.update_dictionary(text)
        self.update_rhymes(text)
        self.update_meter(text)

    def update_dictionary(self, text):
        words = text.split()
        output = ""
        for word in words:
            if word.strip():
                output += f"[b]{word}[/b]\nSuggestions: {', '.join(dictionary.suggest(word)[:3])}\n\n"
        self.dict_tab.text = output or "No suggestions found."

    def update_rhymes(self, text):
        last_word = text.strip().split()[-1] if text.strip() else ""
        rhymes = pronouncing.rhymes(last_word)[:10]
        phones = pronouncing.phones_for_word(last_word)
        output = f"[b]Rhymes for '{last_word}':[/b]\n{', '.join(rhymes)}\n\nPhonetics: {phones[0] if phones else 'N/A'}"
        self.rhyme_tab.text = output or "No rhymes found."

    def update_meter(self, text):
        pattern = []
        for word in text.split():
            phones_list = pronouncing.phones_for_word(word)
            if phones_list:
                stresses = pronouncing.stresses(phones_list[0])
                pattern.extend([int(s) for s in stresses if s.isdigit()])
        self.meter_tab.text = "Stress Pattern:\n" + ' '.join(map(str, pattern)) if pattern else "No stress pattern detected."

class VersePadApp(App):
    def build(self):
        return VersePad()

if __name__ == "__main__":
    VersePadApp().run()
