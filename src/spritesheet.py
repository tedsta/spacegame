import sfml as sf

class SpriteSheet(sf.Sprite):
    def init(self, frames, frames_per_row, frame_delay=0.1):
        self.frames = frames
        self.frames_per_row = frames_per_row
        self.frame_delay = frame_delay
        self.time = 0
        self.frame = 0
        self.start_frame = 0
        self.stop_frame = frames-1
        self.frame_dim = sf.Vector2(self.texture.width/frames_per_row, self.texture.height/(frames/frames_per_row))
        self.loop = True
        self.loop_done = False
        self.set_frame(0)
    
    def update(self, dt):
        self.time += dt                            # Accumulate time
        if self.time >= self.frame_delay:         # Enough time has passed to show the next frame
            self.time -= self.frame_delay
            self.frame += 1                        # Increment the frame
            if self.frame > self.stop_frame:      
                # Loop back to frame start if we need to
                if self.loop:
                    self.frame = self.start_frame
                else:
                    self.frame = self.stop_frame
                    self.loop_done = True
            self.set_frame(self.frame)            # Set the texture rectangle for the frame
    
    def set_frame_loop(self, start, stop, loop=True):
        if start == self.start_frame and stop == self.stop_frame and self.loop and loop == self.loop:
            return
        self.start_frame = start
        self.stop_frame = stop
        self.loop = loop
        self.loop_done = False
        self.frame = self.start_frame
        self.set_frame(self.frame)
        self.time = 0
    
    def set_frame(self, frame):
        x = frame%self.frames_per_row
        y = frame//self.frames_per_row
        position = sf.Vector2(x*self.frame_dim.x, y*self.frame_dim.y)
        self.texture_rectangle = sf.Rectangle(position, self.frame_dim)
