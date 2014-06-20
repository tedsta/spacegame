#!/usr/bin/env python

import unittest
from mock import Mock
from src.path import find_path, _get_available_moves, _manhattan_distance, _get_mov_cost
from src.grid import Grid, WalkDirs

class TestPath(unittest.TestCase):

    def setUp(self):
        self.grid = Grid(4, 3)
        self.upwalkdirs = WalkDirs(up_left=True, up=True, up_right=True,
                    left=True, right=True, down_left=False,
                    down=False, down_right=False)
        self.grid.set(1, 1, self.upwalkdirs)
        self.position = (1, 1)

    def test_path_when_destination_is_same_as_position(self):
        destination = (1, 1)
        expected = [(1, 1), (1, 1)]
        actual = find_path(self.grid, self.position, destination)
        self.assertEqual(actual, expected)

    def test_path_one_square_up(self):
        destination = (1, 0)
        expected = [(1, 1), (1, 0)]
        actual = find_path(self.grid, self.position, destination)
        self.assertEqual(actual, expected)
        
    def test_path_one_square_right(self):
        destination = (2, 1)
        expected = [(1, 1), (2, 1)]
        actual = find_path(self.grid, self.position, destination)
        self.assertEqual(actual, expected)
        
    def test_path_one_square_diagonal(self):
        destination = (0, 0)
        expected = [(1, 1), (0, 0)]
        actual = find_path(self.grid, self.position, destination)
        self.assertEqual(actual, expected)

    def test_path_two_squares_right(self):
        destination = (3, 1)
        expected = [(1, 1), (2, 1), (3, 1)]
        actual = find_path(self.grid, self.position, destination)
        # TODO
        #self.assertEqual(actual, expected)"""
   
    def test_get_available_moves(self):
        expected = [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1)]
        actual = _get_available_moves(self.grid, self.position)
        self.assertEqual(actual, expected)

    def test_manhattan_distance(self):
        destination = (4, 2)
        expected = 4
        actual = _manhattan_distance(self.position, destination)
        self.assertEqual(actual, expected)

    def test_get_mov_cost(self):
        destination = (1, 2)
        expected = 10
        actual = _get_mov_cost(self.position, destination)
        self.assertEqual(actual, expected)

##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPath))
    return suite

if __name__ == '__main__':
    unittest.main()
