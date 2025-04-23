from math import sqrt, atan2
from copy import deepcopy

CORNERS = [
    [-27.0, 5.0],
    [26.99, 45.0],
    [27.0, 18.5],
    [-9.49, 45.0],
    [-9.5, 106.21]
]

def get_section_id_of_led(corners, led_nr, total_leds):

    cumulative_distances = compute_cumulative_distances(corners)
    total_distance = cumulative_distances[-1]

    # convert led nr to distance
    led_dist = led_nr / total_leds * total_distance

    # we now have each element in "cumulative_distances" matching where each element in "corners" ends
    if led_dist < cumulative_distances[0]:
        section_id = 0
    elif led_dist < cumulative_distances[1]:
        section_id = 1
    elif led_dist < cumulative_distances[2]:
        section_id = 2
    elif led_dist < cumulative_distances[3]:
        section_id = 3
    else:
        raise ValueError('LED nr out of bounds')

    return section_id

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

def get_section_ids_of_all_leds(total_leds, x_mirrored=False):
    
    if x_mirrored:
        corners = flip_corners(CORNERS.copy())
    else:
        corners = CORNERS.copy()

    section_ids_strip = list()

    for i in range(total_leds):
        coord = get_section_id_of_led(corners, i, total_leds)
        section_ids_strip.append(coord)

    return section_ids_strip

def get_cart_coordinates_of_all_leds(total_leds, x_mirrored=False):
    
    if x_mirrored:
        corners = flip_corners(CORNERS.copy())
    else:
        corners = CORNERS.copy()

    coords_strip = list()

    for i in range(total_leds):
        coord = get_coordinates_of_led(corners, i, total_leds)
        coords_strip.append(coord)

    return coords_strip

def get_board_coordinates_of_all_leds(total_leds, x_bounds, y_bounds, x_mirrored=False):
    
    if x_mirrored:
        corners = flip_corners(deepcopy(CORNERS))
    else:
        corners = deepcopy(CORNERS)
    
    corners  = get_normalized_corner_coords(corners, x_bounds, y_bounds)
    
    coords_strip = list()

    for i in range(total_leds):
        coord = get_coordinates_of_led(corners, i, total_leds)
        coords_strip.append(coord)

    return coords_strip

def get_spherical_coordinates_of_all_leds(cartesian_coordinates):
    
    spherical_coords = list()
    y_offset = (CORNERS[1][1] + CORNERS[2][1]) / 2

    for x, y in cartesian_coordinates:
        y -= y_offset

        r = sqrt(x**2 + y**2)
        theta = atan2(y, x)
        spherical_coords.append([r, theta])

    return spherical_coords

def get_normalized_corner_coords(corners, x_bounds, y_bounds):
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

        corners[i][0] = x1
        corners[i][1] = y1

    return tuple(corners)

def flip_corners(corners):
    x0_min = min([c[0] for c in corners])
    x0_max = max([c[0] for c in corners])

    for i, coord in enumerate(corners):
        x = coord[0]
        x = x0_max - x + x0_min
        corners[i][0] = x

    return corners

def distance(loc1, loc2):
    dy = loc2[1] - loc1[1]
    dx = loc2[0] - loc1[0]
    dist = sqrt(dy**2 + dx**2)
    return dist

def compute_cumulative_distances(coords):
    distances = list()
    for i in range(len(coords) - 1):
        dist = distance(coords[i], coords[i + 1])
        distances.append(dist)

    # cumulative distances
    cumulative_total = 0
    cumulative_distances = list()
    for i in range(len(distances)):
        cumulative_total += distances[i]
        cumulative_distances.append(cumulative_total)
    
    return cumulative_distances