#!/usr/bin/env python

import unittest
from mock import Mock
from src.path import find_path, _get_available_moves, _manhattan_distance, _get_mov_cost, WalkDirs
from src.grid import Grid

class TestPath(unittest.TestCase):

    def setUp(self):
        """Defines a 4x3 grid with the following layout:

        (0=walkable, X=not walkable, P=position, D=destination)

        0 0 0 D
        0 P X 0
        X X X X
        """
        self.grid = Grid(4, 3)
        pwalkdirs = WalkDirs(up_left=True, up=True, up_right=False,
                    left=True, right=False, down_left=False,
                    down=False, down_right=False)
        self.grid.set(1, 1, pwalkdirs)
        walkdirs_0_0 = WalkDirs(False, False, False, False, True, False, True, True)
        self.grid.set(0, 0, walkdirs_0_0)
        walkdirs_0_1 = WalkDirs(False, True, True, False, True, False, False, False)
        self.grid.set(0, 1, walkdirs_0_1)
        walkdirs_1_0 = WalkDirs(False, False, False, True, True, True, True, False)
        self.grid.set(1, 0, walkdirs_1_0)
        walkdirs_2_0 = WalkDirs(False, False, False, True, True, False, False, False)
        self.grid.set(2, 0, walkdirs_2_0)
        walkdirs_3_0 = WalkDirs(False, False, False, True, False, False, True, False)
        self.grid.set(3, 0, walkdirs_3_0)
        self.position = (1, 1)

    def test_path_when_destination_is_same_as_position(self):
        destination = (1, 1)
        expected = [(1, 1)]
        #actual = find_path(self.grid, self.position, destination)
        #self.assertEqual(actual, expected)

    def test_path_one_square_up(self):
        destination = (1, 0)
        expected = [(1, 1), (1, 0)]
        #actual = find_path(self.grid, self.position, destination)
        #self.assertEqual(actual, expected)
        
    def test_path_one_square_left(self):
        destination = (0, 1)
        expected = [(1, 1), (0, 1)]
        #actual = find_path(self.grid, self.position, destination)
        #self.assertEqual(actual, expected)
        
    def test_path_one_square_diagonal(self):
        destination = (0, 0)
        expected = [(1, 1), (0, 0)]
        #actual = find_path(self.grid, self.position, destination)
        #self.assertEqual(actual, expected)

    def test_path_two_squares_right(self):
        position = (0, 0)
        destination = (2, 0)
        expected = [(0, 0), (1, 0), (2, 0)]
        #actual = find_path(self.grid, position, destination)
        #self.assertEqual(actual, expected)

    def test_whole_path(self):
        destination = (3, 0)
        expected = [(1, 1), (1, 0), (2, 0), (3, 0)]
        actual = find_path(self.grid, self.position, destination)
        self.assertEqual(actual, expected)
   
    def test_get_available_moves(self):
        expected = [(0, 0), (1, 0), (0, 1)]
        actual = _get_available_moves(self.grid, self.position)
        self.assertEqual(actual, expected)

    def test_manhattan_distance(self):
        destination = (4, 2)
        expected = 40
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
