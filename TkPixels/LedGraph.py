from copy import deepcopy
from TkPixels.LedCoordinates import compute_cumulative_distances, flip_corners

def compute_led_nrs_per_intersection(intersections, total_leds):
    # get the coords of all the intersections of a specific strip
    intersection_letters_per_strip = ['A', 'E', 'G', 'L', 'D', 'G', 'H', 'J', 'M'] # only left strip, because the right one has the same outcome

    intersection_coords = [intersections[letter]['coords'] for letter in intersection_letters_per_strip]

    cumulative_distances = compute_cumulative_distances(intersection_coords, count_zero=True)
    total_dist = cumulative_distances[-1]
    led_nrs_per_intersection = [int(dist / total_dist * total_leds) for dist in cumulative_distances]

    return led_nrs_per_intersection

def get_graph_section_ids_of_all_leds(led_nrs_per_intersection, total_leds):

    graph_section_ids_strip = list()
    led_nrs_per_intersection.pop(0)

    section_id = 0
    for i in range(total_leds):
        while section_id < len(led_nrs_per_intersection) and i >= led_nrs_per_intersection[section_id]:
            section_id += 1
        if section_id >= len(led_nrs_per_intersection):
            raise ValueError('LED nr out of bounds')
        graph_section_ids_strip.append(section_id)

    return graph_section_ids_strip

def get_intersection_of_coords(coord_11, coord_12, coord_21, coord_22):
    # compute intersection [x_int, y_int] of y1(x) = a1*x + b2 and y2(x) = a2*x + b2
    # a = Dy / Dx
    # b = y - a1*x
    # x_int = - (b2 - b1) / (a2 - a1)
    # y_int = a1 * x_int + b1

    a1 = (coord_12[1] - coord_11[1]) / (coord_12[0] - coord_11[0])
    b1 = coord_11[1] - a1 * coord_11[0]
    a2 = (coord_22[1] - coord_21[1]) / (coord_22[0] - coord_21[0])
    b2 = coord_21[1] - a2 * coord_21[0]

    x_int = - (b2 - b1) / (a2 - a1)
    y_int = a1 * x_int + b1

    return [x_int, y_int]

def compute_graph(corners, total_leds):
    flipped_corners = flip_corners(deepcopy(corners))

    ### DEFINE X/Y COORDS ###
    # top/bottom diamond
    x_0 = 0
    # right diamond / right upper part
    x_1 = -corners[4][0]
    # right side
    x_2 = corners[2][0]

    # bottom
    y_0 = corners[0][1]
    # lower right/left corner
    y_1 = corners[2][1]
    # bottom diamond
    intersection = get_intersection_of_coords(corners[0], corners[1], flipped_corners[0], flipped_corners[1])
    y_2 = round(intersection[1], 1)
    # left/right diamond
    intersection = get_intersection_of_coords(corners[0], corners[1], corners[2], corners[3])
    y_3 = round(intersection[1], 1)
    # top diamond
    intersection = get_intersection_of_coords(corners[2], corners[3], flipped_corners[2], flipped_corners[3])
    y_4 = round(intersection[1], 1)
    # upper right/left corner / bottom upper part
    y_5 = corners[1][1]
    # top
    y_6 = corners[4][1]

    ### DEFINE INTERSECTION COORDINATES
    graph = {
        'A': {'coords': [-x_2, y_0]},
        'B': {'coords': [x_2, y_0]},
        'C': {'coords': [-x_2, y_1]},
        'D': {'coords': [x_2, y_1]},
        'E': {'coords': [x_0, y_2]},
        'F': {'coords': [-x_1, y_3]},
        'G': {'coords': [x_1, y_3]},
        'H': {'coords': [x_0, y_4]},
        'I': {'coords': [-x_2, y_5]},
        'J': {'coords': [-x_1, y_5]},
        'K': {'coords': [x_1, y_5]},
        'L': {'coords': [x_2, y_5]},
        'M': {'coords': [-x_1, y_6]},
        'N': {'coords': [x_1, y_6]}
    }

    led_nrs_per_intersection = compute_led_nrs_per_intersection(graph, total_leds)

    ### DETERMINE CONNECTIONS
    graph['A']['connections'] = {
        'E': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[0],
            'led_end': led_nrs_per_intersection[1],
            'graph_section': 0
        }
    }
    graph['B']['connections'] = {
        'E': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[0],
            'led_end': led_nrs_per_intersection[1],
            'graph_section': 0
        }
    }
    graph['C']['connections'] = {
        'F': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[4],
            'led_end': led_nrs_per_intersection[5],
            'graph_section': 4
        },
        'I': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[4],
            'led_end': led_nrs_per_intersection[3],
            'graph_section': 3
        }
    }
    graph['D']['connections'] = {
        'G': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[4],
            'led_end': led_nrs_per_intersection[5],
            'graph_section': 4
        },
        'L': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[4],
            'led_end': led_nrs_per_intersection[3],
            'graph_section': 3
        }
    }
    graph['E']['connections'] = {
        'A': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[1],
            'led_end': led_nrs_per_intersection[0],
            'graph_section': 0
        },
        'B': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[1],
            'led_end': led_nrs_per_intersection[0],
            'graph_section': 0
        },
        'F': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[1],
            'led_end': led_nrs_per_intersection[2],
            'graph_section': 1
        },
        'G': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[1],
            'led_end': led_nrs_per_intersection[2],
            'graph_section': 1
        }
    }
    graph['F']['connections'] = {
        'C': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[5],
            'led_end': led_nrs_per_intersection[4],
            'graph_section': 4
        },
        'E': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[2],
            'led_end': led_nrs_per_intersection[1],
            'graph_section': 1
        },
        'H': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[5],
            'led_end': led_nrs_per_intersection[6],
            'graph_section': 5
        },
        'I': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[2],
            'led_end': led_nrs_per_intersection[3],
            'graph_section': 2
        }
    }
    graph['G']['connections'] = {
        'D': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[5],
            'led_end': led_nrs_per_intersection[4],
            'graph_section': 4
        },
        'E': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[2],
            'led_end': led_nrs_per_intersection[1],
            'graph_section': 1
        },
        'H': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[5],
            'led_end': led_nrs_per_intersection[6],
            'graph_section': 5
        },
        'L': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[2],
            'led_end': led_nrs_per_intersection[3],
            'graph_section': 2
        }
    }
    graph['H']['connections'] = {
        'F': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[6],
            'led_end': led_nrs_per_intersection[5],
            'graph_section': 5
        },
        'G': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[6],
            'led_end': led_nrs_per_intersection[5],
            'graph_section': 5
        },
        'J': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[6],
            'led_end': led_nrs_per_intersection[7],
            'graph_section': 6
        },
        'K': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[6],
            'led_end': led_nrs_per_intersection[7],
            'graph_section': 6
        }
    }
    graph['I']['connections'] = {
        'C': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[3],
            'led_end': led_nrs_per_intersection[4],
            'graph_section': 3
        },
        'F': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[3],
            'led_end': led_nrs_per_intersection[2],
            'graph_section': 2
        }
    }
    graph['J']['connections'] = {
        'H': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[7],
            'led_end': led_nrs_per_intersection[6],
            'graph_section': 6
        },
        'M': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[7],
            'led_end': led_nrs_per_intersection[8],
            'graph_section': 7
        }
    }
    graph['K']['connections'] = {
        'H': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[7],
            'led_end': led_nrs_per_intersection[6],
            'graph_section': 6
        },
        'N': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[7],
            'led_end': led_nrs_per_intersection[8],
            'graph_section': 7
        }
    }
    graph['L']['connections'] = {
        'D': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[3],
            'led_end': led_nrs_per_intersection[4],
            'graph_section': 3
        },
        'G': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[3],
            'led_end': led_nrs_per_intersection[2],
            'graph_section': 2
        }
    }
    graph['M']['connections'] = {
        'J': {
            'strip_nr': 1,
            'led_start': led_nrs_per_intersection[8],
            'led_end': led_nrs_per_intersection[7],
            'graph_section': 7
        }
    }
    graph['N']['connections'] = {
        'K': {
            'strip_nr': 0,
            'led_start': led_nrs_per_intersection[8],
            'led_end': led_nrs_per_intersection[7],
            'graph_section': 7
        }
    }

    return graph