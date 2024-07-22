import unittest
from unittest.mock import MagicMock
import tkinter as tk
from game.main import create_home_screen, create_mode_selection_screen, transition_to_game, transition_to_mode_selection, spawn_enemies

class TestMain(unittest.TestCase):

    def setUp(self):
        # Setup code to run before each test
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=1000, height=800)
        self.canvas.pack()

    def test_create_home_screen(self):
        create_home_screen(self.canvas)
        # Test if the title and button were created
        title = self.canvas.find_withtag("title")
        self.assertTrue(title, "Title text not found")
        button = self.canvas.find_withtag("button")
        self.assertTrue(button, "Start button not found")

    def test_create_mode_selection_screen(self):
        create_mode_selection_screen(self.canvas)
        # Test if the mode selection title and buttons were created
        title = self.canvas.find_withtag("title")
        self.assertTrue(title, "Mode selection title not found")
        buttons = self.canvas.find_withtag("mode_button")
        self.assertTrue(buttons, "Mode buttons not found")

    def test_transition_to_game(self):
        # Mock the Player and enemies
        self.mock_player = MagicMock()
        self.mock_player.move = MagicMock()
        self.mock_player.shoot_laser = MagicMock()

        # Replace Player and spawn_enemies with mocks
        with unittest.mock.patch('game.main.Player', return_value=self.mock_player), \
             unittest.mock.patch('game.main.spawn_enemies'):

            transition_to_game("Orbital Defense")
            
            # Test if player initialization and enemy spawning are called
            self.mock_player.move.assert_called()
            unittest.mock.patch('game.main.spawn_enemies').assert_called()

    def tearDown(self):
        # Cleanup code to run after each test
        self.root.destroy()

if __name__ == "__main__":
    unittest.main()
