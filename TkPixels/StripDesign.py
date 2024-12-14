from collections.abc import MutableSequence

class Strip(MutableSequence):
    def __init__(self, num_pixels, brightness, canvas, canvas_index_offset):
        self.num_pixels = num_pixels
        self.brightness = brightness
        self.list = [(0, 0, 0)]*num_pixels
        self.canvas = canvas
        self.offset = canvas_index_offset

        return
    
    def __getitem__(self, i):
        return self.list[i]
    
    def __setitem__(self, i, v):
        self.check(v)
        self.list[i] = v
        self.canvas.itemconfig(i + self.offset, fill = ('#%02x%02x%02x' % v))
    
    def __delitem__(self, i):
        raise RuntimeError("Deletion not allowed")
    
    def __len__(self): 
        return len(self.list)
    
    def check(self, v):
        if not isinstance(v, tuple):
            raise TypeError("Value must be a tuple")
    
    def insert(self):
        raise RuntimeError("Insertion not allowed")
        
    def show(self):
        self.canvas.update()
    
    def fill(self, v):
        self.check(v)
        for i in range(self.num_pixels):
            self.__setitem__(i, v)