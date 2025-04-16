import json
from TkPixels.LedCoordinates import *

NUM_PIXELS = 120
PIXEL_RADIUS = 10
X_BOUNDS = (2*PIXEL_RADIUS, 410 - 2*PIXEL_RADIUS)
Y_BOUNDS = (2*PIXEL_RADIUS, 780 - 2*PIXEL_RADIUS)
FILE_PATH = "data/led_coordinates.json"

# Get LED indices
led_indices_r = [[0, i] for i in range(NUM_PIXELS)]
led_indices_l = [[1, j] for j in range(NUM_PIXELS)]
led_indices = led_indices_r + led_indices_l

# Get Section IDs for each 
section_ids_r = get_section_ids_of_all_leds(
    NUM_PIXELS,
    x_mirrored = False
)
section_ids_l = get_section_ids_of_all_leds(
    NUM_PIXELS,
    x_mirrored = True
)
section_ids_r = [[0, id_r] for id_r in section_ids_r]
section_ids_l = [[1, id_l] for id_l in section_ids_l]
section_ids = section_ids_r + section_ids_l

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

# Get Spherical coordinates
coords_spherical = get_spherical_coordinates_of_all_leds(coords_cart)

# Save coordinates to JSON
led_coordinates = {
    'indices': led_indices,
    'section_ids': section_ids,
    'coords_board': coords_board,
    'coords_cart': coords_cart,
    'coords_spherical': coords_spherical
}

with open(FILE_PATH, "w") as outfile: 
    json.dump(led_coordinates, outfile)