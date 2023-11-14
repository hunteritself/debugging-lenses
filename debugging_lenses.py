# debugging_lenses.py

from kivy.core.window import Window
from kivy.graphics import Color, Line, Ellipse
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

from debugging_control_panel import DebuggingControlPanel


class DebuggingLens(FloatLayout):
    lens_position = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(DebuggingLens, self).__init__(**kwargs)
        # The current instance
        DebuggingLens.current_instance = self

        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.lens_position = self.pos
        self.bind(lens_position=self.update_label_position)

        self.debug_settings = {
            "show_class": True,
            "show_name": True,
            "show_position": True,
            "show_size": True,
            "show_font": True,
            "show_font_size": True,
            "show_background_color": True,
            "show_font_color": True,
            # Add the property setting
            "show_properties": False,
            # Add the event log setting
            "show_event_log": False
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
        # The size of the label is 80% of the lens diameter
        label_size = (self.lens_diameter * 0.8, self.lens_diameter * 0.8)
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
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'tab':
            self.toggle_visibility()
        elif keycode[1] in ['up', 'down']:
            increase = keycode[1] == 'up'
            self.update_lens_position_and_size(increase=increase)
        return True

    def toggle_visibility(self):
        self.visible = not getattr(self, 'visible', False)
        self.opacity = 1 if self.visible else 0

        if self.control_panel:
            self.control_panel.opacity = 1 if self.visible else 0

    def update_lens_position_and_size(self, increase=True):
        # Calculate the current center of the lens
        current_center_x = self.lens_position[0] + self.lens_radius
        current_center_y = self.lens_position[1] + self.lens_radius

        # Update the lens diameter
        change = 10 if increase else -10
        new_diameter = max(10, self.lens_diameter + change)
        self.lens_diameter = new_diameter
        self.lens_radius = self.lens_diameter / 2

        # Calculate the new center of the lens
        new_x = current_center_x - self.lens_radius
        new_y = current_center_y - self.lens_radius

        # Update the lens position
        self.pos = (new_x, new_y)
        self.lens_position = (new_x, new_y)

        # Update the display
        self.draw_lens_and_handle()
        self.update_info()

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

    def update_label_position(self, instance, value):
        label_x, label_y = self.calculate_label_pos()
        self.info_label.pos = (label_x, label_y)

    def on_touch_move(self, touch):
        if self.is_touch_on_control_panel(touch):
            return False

        if self.collide_point(*touch.pos):
            self.lens_position = touch.pos
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
            self.info_label.text = "No Widget"
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

        # Add the property info
        if self.debug_settings["show_properties"]:
            info_text += "\nProperties:\n"
            for property_name in widget.properties():
                if property_name in ['parent', 'text']:
                    value = getattr(widget, property_name)
                    if value is not None:
                        info_text += f"{property_name.capitalize()}: {value}\n"

        # Add the event info
        if self.debug_settings["show_event_log"]:
            info_text += "\nEvent Log:\n" + DebuggingLens.get_event_log()

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

    def refresh_display(self):
        if self.selected_widget:
            self.construct_info_text(self.selected_widget)

    # Store the event log
    event_log = []

    @staticmethod
    def log_event(message):
        print("Event Logged:", message)
        DebuggingLens.event_log.append(message)

    @staticmethod
    def get_event_log():
        formatted_log = "\n".join(DebuggingLens.event_log)
        return formatted_log

    @staticmethod
    def get_current_instance():
        return DebuggingLens.current_instance

    def is_touch_on_control_panel(self, touch):
        if self.control_panel and self.control_panel.collide_point(*touch.pos):
            return True
        return False


class TrackedButton(Button):
    def on_touch_down(self, touch):
        # Check if the touch is on the button
        if self.collide_point(*touch.pos):
            # If it is, record the event
            DebuggingLens.log_event(f"on_touch_down at {touch.pos} on {self.text}")

            # Refresh the display
            lens_instance = DebuggingLens.get_current_instance()
            if lens_instance:
                lens_instance.refresh_display()

            # Return True
            return super().on_touch_down(touch)
        # If not, return False
        return False