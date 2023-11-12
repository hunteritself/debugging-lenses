# debugging_lenses.py

from kivy.core.window import Window
from kivy.graphics import Color, Line, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

from debugging_control_panel import DebuggingControlPanel


class DebuggingLens(FloatLayout):
    def __init__(self, **kwargs):
        super(DebuggingLens, self).__init__(**kwargs)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.debug_settings = {
            "show_class": True,
            "show_name": True,
            "show_position": True,
            "show_size": True,
            "show_font": True,
            "show_font_size": True,
            "show_background_color": True,
            "show_font_color": True
        }

        # Check if the debugging lens is active
        self.active = True

        # Check if the checkbox is clicked
        self.checkbox_changed = False

        self.lens_diameter = 200
        self.lens_radius = self.lens_diameter / 2
        self.handle_length = 80
        self.handle_width = 5

        # Draw the lens and handle
        self.draw_lens_and_handle()

        # Draw the info label
        label_size = (self.lens_diameter * 0.8, self.lens_diameter * 0.8)  # 标签大小稍小于放大镜直径
        label_x = self.x + (self.lens_diameter - label_size[0]) / 2
        label_y = self.y + (self.lens_diameter - label_size[1]) / 2

        # Draw the info label using canvas.after
        with self.canvas.after:
            self.info_label = Label(text="Debugging Info", size_hint=(None, None), size=label_size,
                                    pos=(label_x, label_y), halign='center', valign='middle', bold=True)
            self.add_widget(self.info_label)

        self.control_panel = DebuggingControlPanel(self)
        self.control_panel.bind(on_dismiss=self.on_control_panel_dismiss)
        self.control_panel.open()

        # Currently selected widget
        self.selected_widget = None
        # Currently highlighted widget
        self.selected_widget_highlight = None

    def draw_lens_and_handle(self):
        with self.canvas.before:
            # Clear the canvas
            self.canvas.before.clear()

            # Draw the lens
            Color(1, 1, 1, 0.4)
            self.lens = Ellipse(size=(self.lens_diameter, self.lens_diameter), pos=self.pos)

            # Draw the handle
            handle_start_x, handle_start_y, handle_end_x, handle_end_y = self.calculate_handle_points()
            Color(0.5, 0.5, 0.5, 1)
            self.handle = Line(points=[handle_start_x, handle_start_y, handle_end_x, handle_end_y], width=self.handle_width)

    def calculate_handle_points(self):
        handle_start_x = self.x + self.lens_radius - self.handle_width / 2
        handle_start_y = self.y
        handle_end_x = handle_start_x
        handle_end_y = handle_start_y - self.handle_length
        return handle_start_x, handle_start_y, handle_end_x, handle_end_y

    def calculate_label_pos(self):
        label_x = self.x + (self.lens_diameter - self.info_label.width) / 2
        label_y = self.y + (self.lens_diameter - self.info_label.height) / 2
        return label_x, label_y

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.pos = touch.pos
            self.lens.pos = self.pos

            # Update the handle position
            handle_start_x = self.x + self.lens_radius - self.handle_width / 2
            handle_start_y = self.y
            handle_end_x = handle_start_x
            handle_end_y = handle_start_y - self.handle_length
            self.handle.points = [handle_start_x, handle_start_y, handle_end_x, handle_end_y]

            # Update the info label position
            label_x = self.x + (self.lens_diameter - self.info_label.width) / 2
            label_y = self.y + (self.lens_diameter - self.info_label.height) / 2
            self.info_label.pos = (label_x, label_y)

            self.update_info()

            # Update the highlighted widget
            self.highlight_selected_widget()

            # Check if the control panel is open
            if not self.control_panel.is_open:
                self.control_panel.open()

        return super(DebuggingLens, self).on_touch_move(touch)

    def update_info(self):
        if not self.active:
            return

        # Get the center of the lens
        lens_center_x = self.x + self.lens_radius
        lens_center_y = self.y + self.lens_radius

        # Iterate through all the widgets
        covered_widgets = [child for child in self.parent.children if self.collide_widget(child) and child != self]

        if covered_widgets:
            closest_widget = None
            min_distance = float('inf')
            for widget in covered_widgets:
                center_x, center_y = widget.center
                distance = ((center_x - lens_center_x) ** 2 + (center_y - lens_center_y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_widget = widget

            # If the checkbox is clicked, update the info label
            if not self.checkbox_changed or closest_widget == self.selected_widget:
                self.selected_widget = closest_widget
                self.construct_info_text(closest_widget)
                self.highlight_selected_widget()
            self.checkbox_changed = False
        else:
            self.info_label.text = "No widget"
            self.selected_widget = None
            self.highlight_selected_widget()

    def construct_info_text(self, widget):
        info_text = ""
        if self.debug_settings["show_class"]:
            info_text += f"Class: {widget.__class__.__name__}\n"

        if self.debug_settings["show_name"] and hasattr(widget, 'name'):
            info_text += f"Name: {widget.name}\n"

        if self.debug_settings["show_position"]:
            info_text += f"Position: {widget.pos}\n"

        if self.debug_settings["show_size"]:
            info_text += f"Size: {widget.size}\n"

        if self.debug_settings["show_font"] and hasattr(widget, 'font_name'):
            info_text += f"Font: {widget.font_name}\n"

        if self.debug_settings["show_font_size"] and hasattr(widget, 'font_size'):
            info_text += f"Font Size: {widget.font_size}\n"

        if self.debug_settings["show_background_color"] and hasattr(widget, 'background_color'):
            info_text += f"Background Color: {widget.background_color}\n"

        if self.debug_settings["show_font_color"] and hasattr(widget, 'color'):
            info_text += f"Font Color: {widget.color}\n"

        self.info_label.text = info_text

    def on_control_panel_dismiss(self, instance):
        Window.remove_widget(self.control_panel)
        self.control_panel = DebuggingControlPanel(self)

    def toggle_debug_setting(self, setting_name, value):
        self.debug_settings[setting_name] = value
        self.checkbox_changed = True
        if self.selected_widget:
            self.construct_info_text(self.selected_widget)

    def highlight_selected_widget(self):
        # Remove the previous highlight
        if self.selected_widget_highlight:
            self.canvas.after.remove(self.selected_widget_highlight)

        if self.selected_widget:
            with self.canvas.after:
                Color(1, 0, 0, 1)
                self.selected_widget_highlight = Line(rectangle=self.selected_widget.pos + self.selected_widget.size, width=2)
        else:
            self.selected_widget_highlight = None