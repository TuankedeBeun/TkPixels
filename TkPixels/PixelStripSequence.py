from time import sleep
from collections.abc import MutableSequence
from rpi_ws281x import ws, Color, PixelStrip

class Strip(MutableSequence):
    def __init__(self, pin, dma, channel, brightness=128, num_pixels=120, frequency_hz=800000, invert=False, strip_type=ws.WS2811_STRIP_RGB):
        self.num_pixels = num_pixels
        self._strip = PixelStrip(num_pixels, pin, frequency_hz,
                                dma, invert, brightness,
                                channel, strip_type)
        self._strip.begin()

        return
    
    def __getitem__(self, i):
        return self._strip.getPixelColor(i)
    
    def __setitem__(self, i, v):
        self.check(v)
        self._strip.setPixelColor(i, Color(*v))
    
    def __delitem__(self, i):
        raise RuntimeError("Deletion not allowed")
    
    def __len__(self): 
        return self.num_pixels
    
    def check(self, v):
        if not isinstance(v, tuple):
            raise TypeError("Value must be a tuple")
    
    def insert(self):
        raise RuntimeError("Insertion not allowed")
        
    def show(self):
        self._strip.show()
        sleep(0.007) # mandatory sleep to process buffer in channel
    
    def fill(self, v):
        self.check(v)
        for i in range(self.num_pixels):
            self.__setitem__(i, v)