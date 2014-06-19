#!/usr/bin/env python

import unittest
from mock import Mock
from src.path import find_path

class TestPath(unittest.TestCase):

    def setUp(self):
        self.grid = Mock()
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
        destination = (2, 2)
        expected = [(1, 1), (2, 2)]
        actual = find_path(self.grid, self.position, destination)
        self.assertEqual(actual, expected)

    def test_path_two_squares_right(self):
        destination = (3, 1)
        expected = [(1, 1), (2, 1), (3, 1)]
        actual = find_path(self.grid, self.position, destination)
        # TODO
        #self.assertEqual(actual, expected)
       
        
##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPath))
    return suite

if __name__ == '__main__':
    unittest.main()
