from collections.abc import MutableSequence
import tkinter as tk
from time import sleep
from math import sqrt

class Design(MutableSequence):
    def __init__(self, num_pixels, brightness):
        self.num_pixels = num_pixels
        self.brightness = brightness
        self.list = [(0, 0, 0)]*num_pixels
        
        self.root = tk.Tk(screenName='LED strip')
        self.width = 500 #self.root.winfo_screenwidth()
        self.height = 800 #self.root.winfo_screenheight()
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, -10, 0))
        self.canvas = tk.Canvas(master = self.root, 
                                width = self.width, 
                                height = self.height)
        self.canvas.configure(background='black')
        self.canvas.pack()
        
        self.pixelradius = 5
        x_bounds = (self.pixelradius, self.width - self.pixelradius)
        y_bounds = (self.pixelradius, self.height - self.pixelradius)
        self.coords_r = get_coordinates_of_all_leds(
            self.num_pixels,
            x_bounds,
            y_bounds,
            x_mirrored = False
        )
        self.coords_l = get_coordinates_of_all_leds(
            self.num_pixels,
            x_bounds,
            y_bounds,
            x_mirrored = True
        )

        self.draw()
        
        return
    
    def __getitem__(self, i): 
        return self.list[i]
    
    def __setitem__(self, i, v):
        self.check(v)
        self.list[i] = v
        self.canvas.itemconfig(i + 1, fill = ('#%02x%02x%02x' % v))
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
        pass
    
    def fill(self, v):
        self.check(v)
        self.list = [v]*self.num_pixels
        self.draw()
    
    def stop(self):
        self.root.destroy()
    
def get_coordinates_of_led(corners, led_nr, total_leds):
    # compute distances
    distances = list()
    for i in range(len(corners) - 1):
        dist = distance(corners[i], corners[i + 1])
        distances.append(dist)
    
    total_distance = sum(distances)

    # cumulative distances
    cumulative_total = 0
    cumulative_distances = list()
    for i in range(len(distances)):
        cumulative_total += distances[i]
        cumulative_distances.append(cumulative_total)

    # convert led nr to distance
    led_dist = led_nr / total_leds * total_distance

    # we now have each element in "cumulative_distances" matching where each element in "corners" ends
    if led_dist < cumulative_distances[0]:
        coord = get_coordinate(corners[0], corners[1], led_dist)
    elif led_dist < cumulative_distances[1]:
        coord = get_coordinate(corners[1], corners[2], (led_dist - cumulative_distances[0]))
    elif led_dist < cumulative_distances[2]:
        coord = get_coordinate(corners[2], corners[3], (led_dist - cumulative_distances[1]))
    elif led_dist < cumulative_distances[3]:
        coord = get_coordinate(corners[3], corners[4], (led_dist - cumulative_distances[2]))
    else:
        raise ValueError('LED nr out of bounds')
    
    return coord

def get_coordinate(point1, point2, dist):
    # get a and b for formula "y(x) = a*x + b" by "a = dy / dx" and "b = y_point1 - a*x_point1"
    x1, y1 = point1
    x2, y2 = point2
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1

    # get dx from distance from "d^2 = dx^2 + dy^2 = dx^2 + (a*dx)^2" --> "d^2 = (a^2 + 1)*dx^2"--> "dx = sqrt(d^2 / (a^2 + 1))"
    dx = sqrt(dist**2 / (a**2 + 1))

    # get x from "x = x_point1 + dx"
    if x2 > x1:
        x = x1 + dx
    else:
        x = x1 - dx

    # get y from "y = a*x + b"
    y = a * x + b
    
    return x, y

def get_coordinates_of_all_leds(total_leds, x_bounds, y_bounds, x_mirrored=False):
    corners  = get_normalized_corner_coords(x_bounds, y_bounds, x_mirrored)
    
    coords_strip1 = list()

    for i in range(total_leds):
        coord = get_coordinates_of_led(corners, i, total_leds)
        coords_strip1.append(coord)

    return coords_strip1

def get_normalized_corner_coords(x_bounds, y_bounds, x_mirrored=False):
    corners = [
        [-32.0, 0.0],
        [31.99, 48.0],
        [32.0, 16.0],
        [-10.99, 48.0],
        [-11.0, 100.0]
    ]

    x0_min = min([c[0] for c in corners])
    x0_max = max([c[0] for c in corners])
    y0_min = min([c[1] for c in corners])
    y0_max = max([c[1] for c in corners])
    x0_range = x0_max - x0_min
    y0_range = y0_max - y0_min

    x_min, x_max = x_bounds
    y_min, y_max = y_bounds
    x1_range = x_max - x_min
    y1_range = y_max - y_min

    for i, coord in enumerate(corners):
        x0, y0 = coord
        x1 = (x0 - x0_min) / x0_range * x1_range + x_min
        y1 = (y0_range - (y0 - y0_min)) / y0_range * y1_range + y_min

        if x_mirrored:
            x1 = x_max - x1 + x_min

        corners[i][0] = x1
        corners[i][1] = y1

        

    print('corner coords:', corners)

    return tuple(corners)

def distance(loc1, loc2):
    dy = loc2[1] - loc1[1]
    dx = loc2[0] - loc1[0]
    dist = sqrt(dy**2 + dx**2)
    return dist