#!/usr/bin/env python

import sfml as sf

class SpriteSheet(sf.Sprite):
    def init(self, frames, frames_per_row, frame_delay=0.1):
        self._frames = frames
        self._frames_per_row = frames_per_row
        self._frame_delay = frame_delay
        self._time = 0
        self._frame = 0
        self._start_frame = 0
        self._stop_frame = frames-1
        self._frame_dim = sf.Vector2(self.texture.width/frames_per_row, self.texture.height/(frames/frames_per_row))
        self._set_frame(0)
    
    def update(self, dt):
        self._time += dt                            # Accumulate time
        if self._time >= self._frame_delay:         # Enough time has passed to show the next frame
            self._time -= self._frame_delay
            self._frame += 1                        # Increment the frame
            if self._frame > self._stop_frame:      # Loop back to frame start if we need to
                self._frame = self._start_frame
            self._set_frame(self._frame)            # Set the texture rectangle for the frame
    
    def set_frame_loop(self, start, stop):
        self._start_frame = start
        self._stop_frame = stop
        self._frame = self._start_frame
        self._time = 0
    
    def _set_frame(self, frame):
        x = frame%self._frames_per_row
        y = frame//self._frames_per_row
        self.texture_rectangle = sf.Rectangle((x*self._frame_dim.x, y*self._frame_dim.y), self._frame_dim)