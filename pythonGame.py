import tkinter as tk
from player import Player

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AstroBlasters")
        self.canvas_width = 800
        self.canvas_height = 800

        # Set up the canvas
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()

        # Create the home screen
        self.create_home_screen()

    def create_home_screen(self):
        """Create the home screen with a title and start button."""
        self.canvas.delete("all")  # Clear any existing content

        # Display the game title
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 - 50,
                                text="AstroBlasters", font=("Helvetica", 40, "bold"), fill="white")

        # Display the start button
        self.start_button = tk.Button(self.root, text="Start Game", font=("Helvetica", 20), command=self.start_game)
        self.start_button_window = self.canvas.create_window(self.canvas_width // 2, self.canvas_height // 2 + 50,
                                                            window=self.start_button)

    def start_game(self):
        """Start the game by removing the home screen and setting up the game."""
        self.canvas.delete("all")
        self.start_button.destroy()
        self.create_game_screen()

    def create_game_screen(self):
        """Set up the game screen with the player and background."""
        # Create the player
        self.player_size = 30
        self.player_x = self.canvas_width // 2
        self.player_y = self.canvas_height // 2
        self.player = Player(self.canvas, self.player_x, self.player_y, self.player_size)

        # Bind key events to the Player instance methods
        self.root.bind('<KeyPress>', self.player.on_key_press)
        self.root.bind('<KeyRelease>', self.player.on_key_release)
        self.canvas.bind('<Motion>', self.player.on_mouse_motion)

        # Start the movement loop
        self.player.move()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()