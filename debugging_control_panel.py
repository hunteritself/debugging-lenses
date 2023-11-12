# debugging_control_panel.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch

from custom_check_box import CustomCheckBox


class DebuggingControlPanel(Popup):
    def __init__(self, debugging_lens, **kwargs):
        super(DebuggingControlPanel, self).__init__(**kwargs)
        self.debugging_lens = debugging_lens
        self.title = 'Debugging Control Panel'
        self.size_hint = (None, None)
        self.size = (600, 600)
        self.pos_hint = {'top': 1, 'right': 1}
        self.auto_dismiss = False

        layout = BoxLayout(orientation='vertical', padding=[10, 10, 10, 10], spacing=10)

        # Make the title bold
        title_label = Label(text=self.title, bold=True, font_size='16sp')
        layout.add_widget(title_label)

        # Add the debugging switch
        self.debugging_switch = Switch(active=True)
        self.debugging_switch.bind(active=self.on_switch_active)
        switch_hbox = BoxLayout()
        switch_hbox.add_widget(Label(text='Enable Debugging'))
        switch_hbox.add_widget(self.debugging_switch)
        layout.add_widget(switch_hbox)

        self.checkbox_items = {
            "show_class": CustomCheckBox(active=self.debugging_lens.debug_settings["show_class"]),

            "show_name": CustomCheckBox(active=self.debugging_lens.debug_settings["show_name"]),

            "show_position": CustomCheckBox(active=self.debugging_lens.debug_settings["show_position"]),

            "show_size": CustomCheckBox(active=self.debugging_lens.debug_settings["show_size"]),

            "show_font": CustomCheckBox(active=self.debugging_lens.debug_settings["show_font"]),

            "show_font_size": CustomCheckBox(active=self.debugging_lens.debug_settings["show_font_size"]),

            "show_background_color": CustomCheckBox(active=self.debugging_lens.debug_settings["show_background_color"]),

            "show_font_color": CustomCheckBox(active=self.debugging_lens.debug_settings["show_font_color"])
        }

        for setting_name, checkbox in self.checkbox_items.items():
            checkbox.bind(active=lambda checkbox, value, setting_name=setting_name: self.debugging_lens.toggle_debug_setting(setting_name, value))
            hbox = BoxLayout(spacing=10)

            display_name = setting_name.replace("show_", "").replace("_", " ").title()

            # Color: green
            checkbox.color = (0, 1, 0, 1)

            label = Label(text=display_name, size_hint_x=None, width=200, halign='left')
            hbox.add_widget(label)
            hbox.add_widget(checkbox)
            layout.add_widget(hbox)

        self.content = layout

    def on_switch_active(self, switch, value):
        # Call if the debugging switch is turned on
        self.debugging_lens.active = value

        if not value:
            self.debugging_lens.info_label.text = ''

    def open(self, *largs):
        super(DebuggingControlPanel, self).open(*largs)
        self.is_open = True

    def dismiss(self, *largs, **kwargs):
        super(DebuggingControlPanel, self).dismiss(*largs, **kwargs)
        self.is_open = False
