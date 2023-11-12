# simple_test.py

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from debugging_lenses import DebuggingLens

class TestApp(App):
    def build(self):
        root = FloatLayout()

        # Add two buttons
        button1 = Button(text="Button 1", size_hint=(None, None), size=(200, 50), pos=(100, 300))
        root.add_widget(button1)

        button2 = Button(text="Button 2", size_hint=(None, None), size=(200, 50), pos=(400, 300))
        root.add_widget(button2)

        # Set the names of the widgets
        button1.name = "Button1"
        button2.name = "Button2"

        # Add the debugging lens
        lens = DebuggingLens()
        root.add_widget(lens)

        return root

if __name__ == '__main__':
    TestApp().run()
