from collections.abc import MutableSequence

class Design(MutableSequence):
    def __init__(self, num_pixels, brightness, canvas):
        self.num_pixels = num_pixels
        self.brightness = brightness
        self.list = [(0, 0, 0)]*num_pixels
        self.canvas = canvas
        return
    
    def __getitem__(self, i): 
        return self.list[i]
    
    def __setitem__(self, i, v):
        self.check(v)
        self.list[i] = v
        self.canvas.itemconfig(i + 1, fill = ('#%02x%02x%02x' % v))
        self.canvas.itemconfig(i + self.num_pixels + 1, fill = ('#%02x%02x%02x' % v))
        self.canvas.update()
    
    def __delitem__(self, i):
        raise RuntimeError("Deletion not allowed")
    
    def __len__(self): 
        return len(self.list)
    
    def check(self, v):
        if not isinstance(v, tuple):
            raise TypeError("Value must be a tuple")
    
    def insert(self):
        raise RuntimeError("Insertion not allowed")
    
    def draw(self):
        # draw LED strip
        
        for coord_list in [self.coords_r, self.coords_l]:
            for (x, y), v in zip(coord_list, self.list):
                x0 = x - self.pixelradius
                x1 = x + self.pixelradius
                y0 = y + self.pixelradius
                y1 = y - self.pixelradius
                self.canvas.create_oval(
                    x0, y0, x1, y1, 
                    width = 1,
                    fill = ('#%02x%02x%02x' % v),
                    outline = 'gray'
                )
        
        self.canvas.update()
        
    def show(self):
        self.draw()
    
    def fill(self, v):
        self.check(v)
        self.list = [v]*self.num_pixels
        self.draw()