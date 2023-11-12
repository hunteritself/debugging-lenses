# multi-class_test.py

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from debugging_lenses import DebuggingLens
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

class MyApp(App):
    def build(self):
        root = FloatLayout()

        # Add a label
        label = Label(text="Test Label", font_size=dp(18), color=get_color_from_hex("#FF0000"),
                      size_hint=(None, None), size=(dp(120), dp(50)), pos=(dp(100), dp(450)))
        root.add_widget(label)

        # Add multiple buttons
        button1 = Button(text="Button 1", font_size=dp(14), background_color=get_color_from_hex("#00FF00"),
                         size_hint=(None, None), size=(dp(100), dp(50)), pos=(dp(300), dp(400)))
        root.add_widget(button1)

        button2 = Button(text="Button 2", font_size=dp(16), background_color=get_color_from_hex("#0000FF"),
                         size_hint=(None, None), size=(dp(100), dp(50)), pos=(dp(500), dp(350)))
        root.add_widget(button2)

        button3 = Button(text="Button 3", font_size=dp(20), background_color=get_color_from_hex("#FFFF00"),
                         size_hint=(None, None), size=(dp(100), dp(50)), pos=(dp(700), dp(300)))
        root.add_widget(button3)

        # Add a slider
        slider = Slider(min=0, max=100, value=50, size_hint=(None, None), size=(dp(200), dp(50)), pos=(dp(400), dp(200)))
        root.add_widget(slider)

        # Set the names of the widgets
        label.name = "Label1"
        button1.name = "Button1"
        button2.name = "Button2"
        button3.name = "Button3"
        slider.name = "Slider1"


        # Add the debugging lens
        lens = DebuggingLens()
        root.add_widget(lens)

        return root

if __name__ == '__main__':
    MyApp().run()
