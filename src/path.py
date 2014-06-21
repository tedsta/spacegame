#!/usr/bin/env python

import sys
import time
import math
from collections import namedtuple

class WalkDirs:
    
    def __init__(self, up_left=False, up=False, up_right=False, left=False, right=False, down_left=False, down=False, down_right=False):
        self.up_left = up_left
        self.up = up
        self.up_right = up_right
        self.left = left
        self.right = right
        self.down_left = down_left
        self.down = down
        self.down_right = down_right

###########################################################

def find_path(grid, position, destination):
    """Returns path as a list of tuples.

    Path starts at position and ends at destination.
    
    Args:
        grid: a WalkGrid whose data values are WalkDir tuples
              of the form (up_left=True, up=True, up_right=False, ...)
        position: an (x, y) tuple
        destination: an (x, y) tuple
    """
    path = []
    squares = {}
    squares[position] = {"parent": None, "mov_cost": 0,
            "man_dist": _manhattan_distance(position, destination),
            "is_open": False}

    moves = _get_available_moves(grid, position)
    for move in moves:
        mov_cost = _get_mov_cost(position, move)
        man_dist = _manhattan_distance(move, destination)
        squares[move] = {"parent": position, "mov_cost": mov_cost, 
                "man_dist": man_dist, "is_open": True}

    current_position = position
    move_history = [current_position]
    while destination not in squares:
        next_move = _next_move(grid, current_position, destination, squares)
        if not next_move:
            # Retrace backward until we can move again
            cant_move = True
            to_remove = []
            for parent_pos in reversed(move_history):
                current_position = parent_pos
                to_remove.append(current_position)
                moves = _get_available_moves(grid, current_position)
                for move in moves:
                    if squares[move]["is_open"]:
                        cant_move = False
                if not cant_move:
                    break
            for r in to_remove:
                move_history.remove(r)
        else:
            current_position = next_move
        move_history.append(current_position)

    current_position = destination
    path.append(current_position)

    while position not in path:
        path.append(squares[current_position]["parent"])
        current_position = squares[current_position]["parent"]

    path = list(reversed(path))
    return path

def _next_move(grid, position, destination, squares):
    moves = _get_available_moves(grid, position)
    min_score = 0
    best_move = None
    for move in moves:
        if not squares[move]["is_open"]:
            continue
        mov_cost = _get_mov_cost(position, move)
        man_dist = _manhattan_distance(move, destination)
        if move not in squares:
            squares[move] = {"parent": position, "mov_cost": mov_cost, 
                    "man_dist": man_dist, "is_open": True}
        score = mov_cost + man_dist
        if min_score == 0 or score < min_score:
            best_move = move
            min_score = score
    if not min_score or not best_move:
        return None
    new_position = best_move
    squares[new_position]["is_open"] = False
    moves = _get_available_moves(grid, new_position)
    for move in moves:
        if move in squares:
            if squares[move]["is_open"]: 
                old_cost = squares[move]["mov_cost"]
                new_cost = squares[new_position]["mov_cost"] +\
                    _get_mov_cost(new_position, move)
                if new_cost < old_cost:
                    squares[move]["parent"] = new_position
        else:
            mov_cost = _get_mov_cost(new_position, move)
            man_dist = _manhattan_distance(move, destination)
            squares[move] = {"parent": new_position, "mov_cost": mov_cost, 
                    "man_dist": man_dist, "is_open": True}
    return new_position


def _get_available_moves(grid, position):
    """Returns a list of allowable moves from a given position.

    Requires that the grid.get() returns a WalkDirs namedtuple.
    """
    x = position[0]
    y = position[1]
    walkdirs = grid.get(x, y)
    moves = []
    if walkdirs.up_left:
        moves.append((x-1, y-1))
    if walkdirs.up:
        moves.append((x, y-1))
    if walkdirs.up_right:
        moves.append((x+1, y-1))
    if walkdirs.left:
        moves.append((x-1, y))
    if walkdirs.right:
        moves.append((x+1, y))
    if walkdirs.down_left:
        moves.append((x-1, y+1))
    if walkdirs.down:
        moves.append((x, y+1))
    if walkdirs.down_right:
        moves.append((x+1, y+1))
    return moves

def _manhattan_distance(position, destination):
    pos_x = position[0]
    pos_y = position[1]
    dest_x = destination[0]
    dest_y = destination[1]
    dist_x = dest_x-pos_x
    dist_y = dest_y-pos_y
    return math.sqrt(dist_x*dist_x + dist_y*dist_y)
    distance = 10*abs(pos_x - dest_x) + 10*abs(pos_y - dest_y)
    return distance

def _get_mov_cost(position, destination):
    """Returns 10 for a left/right/up/down move, 14 for a diagonal move.

    Assumes squares are adjacent; the mov_cost between (1, 1) and (20, 20)
    will be 14, and the mov_cost between (1, 1) and (1, 100) will be 10.
    """
    if position[0] == destination[0]:
        return 10
    elif position[1] == destination[1]:
        return 10
    else:
        return 14
