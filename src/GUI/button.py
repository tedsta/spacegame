import sfml as sf
from src.GUI.element import SpriteElement

from src.rect import contains

class Button(SpriteElement):
    def __init__(self, pos, type, frames, frames_per_row, input): # assumes it's all in one picture
        super().__init__(pos, type, frames, frames_per_row, input)
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        if contains(self.local_bounds, sf.Vector2(x, y)):
            self.sprite.set_frame(2) # down
    
    def on_mouse_button_released(self, button, x, y):
        self.sprite.set_frame(0) # up
            
    def on_mouse_moved(self, position, move):
        if contains(self.local_bounds, sf.Vector2(position.x, position.y)):
            self.sprite.set_frame(1) # hover
        else:
            self.sprite.set_frame(0) # up
            
    def draw(self, target):
        super().draw(target)
