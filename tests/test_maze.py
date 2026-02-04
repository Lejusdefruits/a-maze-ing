import unittest
from models import Maze
from parse import Entry
from generate import generate
from solver import solver


class TestMaze(unittest.TestCase):
    def setUp(self):
        # Create a basic config
        self.entry_data = [
            ("WIDTH", "21"),
            ("HEIGHT", "21"),
            ("ENTRY", "1,1"),
            ("EXIT", "19,19"),
            ("OUTPUT_FILE", "test_output.txt"),
            ("PERFECT", "True"),
            ("RENDER", "ascii"),
            ("SEED", "0")
        ]
        self.entry = Entry(self.entry_data)
        self.maze = Maze(self.entry)

    def test_initialization(self):
        self.assertEqual(self.maze.width, 21)
        self.assertEqual(self.maze.height, 21)
        self.assertEqual(self.maze.entry, (1, 1))
        self.assertEqual(self.maze.grid[1][1].value, 2)  # Entry

    def test_generation(self):
        generate(self.maze)
        # Check that walls are dug (value 0)
        path_count = 0
        for row in self.maze.grid:
            for cell in row:
                if cell.value == 0:
                    path_count += 1
        self.assertGreater(path_count, 0)

    def test_solver(self):
        generate(self.maze)
        self.maze.place_42()
        solution = solver(self.maze)
        self.assertTrue(len(solution) > 0)
        self.assertEqual(solution[-1], self.maze.exit)


if __name__ == '__main__':
    unittest.main()
