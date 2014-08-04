import sfml as sf
from src.GUI.window import Window
from src.GUI.label import Label
from src.GUI.button import Button
from src.rect import contains

class MessageBox(Window): # Basically a hardcoded window
    def __init__(self, pos, width, height, color, message, input):
        super().__init__(pos, width, height, color, input)
        
        self.message = Label(pos, message, input)
        text_width = self.message.text.local_bounds.width
        text_height = self.message.text.local_bounds.height
        self.message.position = self.center - sf.Vector2(text_width/2, text_width/2) # Center text in message box
        self.add_child(self.message)
        
        self.button = Button(self.message.position+sf.Vector2(0, 30), "button", 3, 3, input)
        button_width = self.button.local_bounds.width
        button_height = self.button.local_bounds.height
        self.button.position = sf.Vector2(self.center.x, height-52) - sf.Vector2(button_width/2, button_width/2) # Center button in message box
        self.add_child(self.button)
        
        # TODO: when button is clicked, delete this instance