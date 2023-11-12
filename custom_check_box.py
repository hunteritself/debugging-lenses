from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Line

class CustomCheckBox(CheckBox):
    def __init__(self, **kwargs):
        super(CustomCheckBox, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        checkbox_size = min(self.size) * 1
        checkbox_pos = (self.x + self.width / 2 - checkbox_size / 2,
                        self.y + self.height / 2 - checkbox_size / 2)

        self.canvas.after.clear()
        with self.canvas.after:
            # Set the boarder color to white
            Color(1, 1, 1, 1)
            Line(rectangle=(checkbox_pos[0], checkbox_pos[1], checkbox_size, checkbox_size), width=1.5)
