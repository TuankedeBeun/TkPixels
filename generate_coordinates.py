import json
from TkPixels.LedCoordinates import *

NUM_PIXELS = 60
X_BOUNDS = (0, 500)
Y_BOUNDS = (0, 750)
FILE_PATH = "data/led_coordinates.json"

# Get LED indices
led_indices_r = [[0, i] for i in range(NUM_PIXELS)]
led_indices_l = [[1, j] for j in range(NUM_PIXELS)]
led_indices = led_indices_r + led_indices_l

# Get Board coordinates
coords_board_r = get_board_coordinates_of_all_leds(
    NUM_PIXELS,
    X_BOUNDS,
    Y_BOUNDS,
    x_mirrored = False
)
coords_board_l = get_board_coordinates_of_all_leds(
    NUM_PIXELS,
    X_BOUNDS,
    Y_BOUNDS,
    x_mirrored = True
)
coords_board = coords_board_r + coords_board_l
print(coords_board[:3])

# Get Cartesian coordinates
coords_cart_r = get_cart_coordinates_of_all_leds(
    NUM_PIXELS,
    x_mirrored = False
)
coords_cart_l = get_cart_coordinates_of_all_leds(
    NUM_PIXELS,
    x_mirrored = True
)
coords_cart = coords_cart_r + coords_cart_l
print(coords_cart[:3])

# Save coordinates to JSON
led_coordinates = {
    'indices': led_indices,
    'coords_board': coords_board,
    'coords_cart': coords_cart
}

with open(FILE_PATH, "w") as outfile: 
    json.dump(led_coordinates, outfile)