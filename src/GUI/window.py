import sfml as sf
from src.GUI.element import Element

from src.rect import contains

class Window(Element):
    def __init__(self, pos, width, height, color, input):
        super().__init__(pos, input)
        self.width = width
        self.height = height
        self.center = sf.Vector2(width/2, height/2)
        
        self.vertices = sf.VertexArray(sf.PrimitiveType.QUADS, 4)
        self.vertices[0].position = sf.Vector2(pos.x, pos.y)
        self.vertices[1].position = sf.Vector2(pos.x+self.width, pos.y)
        self.vertices[2].position = sf.Vector2(pos.x+self.width, pos.y+self.height)
        self.vertices[3].position = sf.Vector2(pos.x, pos.y+self.height)
        
        for i in range(0, 4):
            self.vertices[i].color = color
            
        self.local_bounds = sf.Rectangle(pos, sf.Vector2(width, height))
        
        self.mouse_state = 'up'
        
    def make_position_dirty(self):
        self.position_dirty = True
        for child in self.children:
            child.position_dirty = True
            
        self.recalculate_position()
        
    def recalculate_position(self):
        for child in self.children:
            child.local_bounds.position = self.vertices[0].position + child.position
            child.position_dirty = False
        self.position_dirty = False
        
    def add_child(self, element):
        self.children.append(element)
        element.parent = self
        self.recalculate_position()
        
    def remove_child(self, element):
        self.children.remove(element)
        del element
        
    def move(self, x, y):
        self.vertices[0].position += sf.Vector2(x, y)
        self.vertices[1].position += sf.Vector2(x, y)
        self.vertices[2].position += sf.Vector2(x, y)
        self.vertices[3].position += sf.Vector2(x, y)
        self.local_bounds = self.vertices.bounds
        self.make_position_dirty();
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        self.mouse_state = 'down'
    
    def on_mouse_button_released(self, button, x, y):
        self.mouse_state = 'up'
    
    def on_mouse_moved(self, position, move):
        if contains(self.vertices.bounds, sf.Vector2(position.x, position.y)):
            if self.mouse_state == 'down': # mouse is down
                self.move(move.x, move.y)
          
    def draw(self, target):
        target.draw(self.vertices)
        
        for child in self.children:
            child.draw(target)
            
    def update(self, dt):
        for child in self.children:
            child.update(dt)
