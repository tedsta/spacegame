import sfml as sf
from src.GUI.element import Element
import src.res as res

class Label(Element):
    def __init__(self, pos, text, input):
        super().__init__(pos, input)
        self.text = sf.Text(text, res.font_farmville, 20)
        self.text.position = pos
        self.local_bounds = self.text.local_bounds
        
    def update(self, dt):
        self.text.position = self.local_bounds.position
        
    def draw(self, target):
        target.draw(self.text)
