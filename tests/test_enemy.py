import unittest
from game.enemy import BasicDrone

class TestBasicDrone(unittest.TestCase):

    def setUp(self):
        # Setup code to run before each test
        self.canvas = None  # Mock or dummy canvas for testing
        self.drone = BasicDrone(self.canvas, 150, 150, 100, 100)

    def test_initial_position(self):
        self.assertEqual(self.drone.x, 150)
        self.assertEqual(self.drone.y, 150)

    def test_move(self):
        # Test the move method
        self.drone.move()
        # Check the drone's new position
        # Placeholder check
        self.assertNotEqual(self.drone.x, 150)  # Modify according to actual logic

    def tearDown(self):
        # Cleanup code to run after each test
        self.drone = None

if __name__ == "__main__":
    unittest.main()