# trackedbutton_test.py
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from debugging_lenses import DebuggingLens
from debugging_lenses import TrackedButton

class TestApp(App):
    def build(self):
        root = FloatLayout()

        # Create a tracked button
        tracked_button = TrackedButton(text="Tracked Button", size_hint=(None, None), size=(300, 80), pos=(500, 500))
        root.add_widget(tracked_button)

        # Add the debugging lens
        lens = DebuggingLens()
        root.add_widget(lens)

        return root

if __name__ == '__main__':
    TestApp().run()
