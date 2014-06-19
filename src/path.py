#!/usr/bin/env python

def find_path(grid, position, destination):
    """Returns path as a list of tuples.

    Path starts at position and ends at destination.
    
    Args:
        grid: IDK, good question
        position: an (x, y) tuple
        destination: an (x, y) tuple
    """
    return [position, destination]

def _get_all_adjacent_nodes(position):
    x = position[0]
    y = position[1]
    return [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)]
