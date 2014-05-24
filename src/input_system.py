#!/usr/bin/env python

from abc import ABCMeta, abstractmethod
import sfml as sf

# Abstract key handler interface
class KeyHandler(metaclass=ABCMeta):

    @abstractmethod
    def on_key_pressed(self, key_code):
        pass
    
    @abstractmethod
    def on_key_released(self, key_code):
        pass

# Abstract mouse handler interface
class MouseHandler(metaclass=ABCMeta):

    @abstractmethod
    def on_mouse_button_pressed(self, button, x, y):
        pass
    
    @abstractmethod
    def on_mouse_button_released(self, button, x, y):
        pass
    
    @abstractmethod
    def on_mouse_moved(self, position, move):
        pass

class InputSystem:

    def __init__(self, window):
        self._window = window
        self._old_mouse_pos = sf.Vector2(0, 0)
        self._key_handlers = []
        self._mouse_handlers = []
    
    def handle(self):
        for event in self._window.events:
            # close window: exit
            if type(event) is sf.CloseEvent:
                self._window.close()
            # Keyboard event
            elif type(event) is sf.KeyEvent:
                if event.pressed:
                    for handler in self._key_handlers:
                        handler.on_key_pressed(event.code)
                elif event.released:
                    for handler in self._key_handlers:
                        handler.on_key_released(event.code)
            # Mouse button event
            elif type(event) is sf.MouseButtonEvent:
                if event.pressed:
                    for handler in self._mouse_handlers:
                        handler.on_mouse_button_pressed(event.button, self._old_mouse_pos.x, self._old_mouse_pos.y)
                elif event.released:
                    for handler in self._mouse_handlers:
                        handler.on_mouse_button_released(event.button, self._old_mouse_pos.x, self._old_mouse_pos.y)
            # Mouse move event
            elif type(event) is sf.MouseMoveEvent:
                for handler in self._mouse_handlers:
                    handler.on_mouse_moved(event.position, event.position-self._old_mouse_pos)
                self._old_mouse_pos = event.position # Update the old mouse position
    
    def add_key_handler(self, handler):
        self._key_handlers.append(handler)
    
    def add_mouse_handler(self, handler):
        self._mouse_handlers.append(handler)