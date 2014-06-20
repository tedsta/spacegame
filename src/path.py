#!/usr/bin/env python

def find_path(grid, position, destination):
    """Returns path as a list of tuples.

    Path starts at position and ends at destination.
    
    Args:
        grid: a WalkGrid whose data values are WalkDir tuples
              of the form (up_left=True, up=True, up_right=False, ...)
        position: an (x, y) tuple
        destination: an (x, y) tuple
    """
    path = [position]

    # do stuff

    path.append(destination)
    return path

def _get_available_moves(grid, position):
    x = position[0]
    y = position[1]
    moves = []
    walkdirs = grid.get(x, y)
    for direction, allowed in vars(walkdirs).items():
        if allowed:
            moves.append(_get_coordinates(position, direction))
    return moves

def _get_coordinates(position, direction):
    x = position[0]
    y = position[1]
    if direction == "up_left":
        return (x-1, y-1)
    elif direction == "up":
        return (x, y-1)
    elif direction == "up_right":
        return (x+1, y-1)
    elif direction == "left":
        return (x-1, y)
    elif direction == "right":
        return (x+1, y)
    elif direction == "down_left":
        return (x-1, y+1)
    elif direction == "down":
        return (x, y+1)
    elif direction == "down_right":
        return (x+1, y+1)

def _manhattan_distance(position, destination):
    pos_x = position[0]
    pos_y = position[1]
    dest_x = destination[0]
    dest_y = destination[1]
    distance = abs(pos_x - dest_x) + abs(pos_y - dest_y)
    return distance
