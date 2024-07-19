import tkinter as tk
from player import Player

# Create the main window
root = tk.Tk()
root.title("AstroBlasters")

# Set up the canvas
canvas_width = 1000
canvas_height = 800
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

def create_home_screen(canvas):
    # Draw the title of the game
    canvas.create_text(canvas_width // 2, canvas_height // 2 - 50,
                       text="AstroBlasters", font=("Helvetica", 48, "bold"), fill="#FFA500", tags="title")

    # Draw the start button
    button = tk.Button(root, text="Start", command=transition_to_game, font=("Helvetica", 24, "bold"), bg="#444", fg="white")
    button_window = canvas.create_window(canvas_width // 2, canvas_height // 2 + 50, window=button, tags="button")

def transition_to_game():
    canvas.delete("all")  # Clear the home screen
    # Initialize the game elements
    player_size = 30
    player_x = canvas_width // 2
    player_y = canvas_height // 2
    player = Player(canvas, player_x, player_y, player_size)
    
    # Bind key events to the Player instance methods
    root.bind('<KeyPress>', player.on_key_press)
    root.bind('<KeyRelease>', player.on_key_release)
    canvas.bind('<Motion>', player.on_mouse_motion)

    # Start the movement loop
    player.move()

# Create the home screen
create_home_screen(canvas)

# Run the main loop
root.mainloop()