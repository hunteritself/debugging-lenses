# Transparent Debugging Lenses for Kivy

## Overview
The "Transparent Debugging Lenses" is a project for CS6456 to enhance the debugging process in Kivy GUIs development. It provides an interactive, real-time visualization tool that displays various properties of UI components and their relationships within Kivy applications.

## Integrate and Utilize
To use the Transparent Debugging Lenses, ensure Python and Kivy are installed in your environment. This project is compatible with Python 3.10 and Kivy 2.2.1. To integrate Transparent Debugging Lenses into your Kivy application:
1. Import the `DebuggingLens` class:
```python
from debugging_lenses import DebuggingLens
```
2. Add the DebuggingLens widget to your Kivy layout:
```python
lens = DebuggingLens()
root.add_widget(lens)
```

## Features
* **Widget Information Display**: Displays details such as class name, instance name, position, size, font attributes, and color information of Kivy widgets.
* **Control Panel Functionalities**: Offers customizable debugging options to choose the information displayed by the lens.
* **Interactive Lens and Control Panel Management**: Users can toggle the lens and panel visibility and dynamically resize them using keyboard inputs.
* **Lens Movement**: Facilitates easy movement of the lens across the UI using mouse drag actions or keyboard controls.
* **Highlight Selected Widget**: Highlights the focused widget with a bold red border for enhanced visibility.
* **Enhanced Property Visualization**: Supports customizable display of additional widget properties.
* **Event Log Display**: Captures and displays event logs, aiding in understanding UI interactions.

## Keyboard Shortcuts
* `Tab`: Toggle the visibility of the lens and control panel.
* `Arrow Keys`: Resize the lens (left/right) and control panel (up/down).
* `W/A/S/D`: Move the lens up/left/down/right.