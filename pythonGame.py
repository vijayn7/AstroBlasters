import math
import tkinter as tk
from player import Player
from enemy import BasicDrone, FastScout, ArmoredTank, FighterJet, CamouflagedStealth, SuicideBomber, EliteGuardian, SwarmDrone
import random

# Create the main window
root = tk.Tk()
root.title("AstroBlasters")

# Set up the canvas
canvas_width = 1000
canvas_height = 800
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

enemies = []  # Global list to hold enemies

def create_home_screen(canvas):
    # Draw the title of the game
    canvas.create_text(canvas_width // 2, canvas_height // 2 - 50,
                       text="AstroBlasters", font=("Helvetica", 48, "bold"), fill="#FFA500", tags="title")

    # Draw the start button
    start_button = tk.Button(root, text="Start", command=transition_to_mode_selection, font=("Helvetica", 24, "bold"), bg="#444", fg="white", relief="raised", padx=10, pady=5)
    start_button_window = canvas.create_window(canvas_width // 2, canvas_height // 2 + 50, window=start_button, tags="button")

def create_mode_selection_screen(canvas):
    # Draw background rectangle
    canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill="black", outline="white", width=2)

    # Draw the mode selection title
    canvas.create_text(canvas_width // 2, canvas_height // 2 - 150,
                       text="Select Game Mode", font=("Helvetica", 36, "bold"), fill="#FFA500", tags="title")

    # Draw mode buttons horizontally
    modes = ["Orbital Defense", "Mode 2", "Mode 3"]
    button_width = 150
    spacing = button_width + 10
    total_buttons_width = button_width * len(modes) + spacing * (len(modes) - 1)
    start_x = (canvas_width - total_buttons_width) // 2
    center_y = canvas_height // 2 + 50

    for idx, mode in enumerate(modes):
        button = tk.Button(root, text=mode, command=lambda m=mode: transition_to_game(m), font=("Helvetica", 18, "bold"), bg="#333", fg="white", relief="raised", padx=10, pady=5, width=button_width // 10)
        button_window = canvas.create_window(start_x + idx * (button_width + spacing) + button_width // 2, center_y, window=button, tags="mode_button")

def transition_to_mode_selection():
    canvas.delete("all")  # Clear the home screen
    create_mode_selection_screen(canvas)

def transition_to_game(mode):
    canvas.delete("all")  # Clear the mode selection screen
    # Initialize the game elements based on selected mode
    player_size = 30
    player_x = canvas_width // 2
    player_y = canvas_height // 2
    player = Player(canvas, player_x, player_y, player_size, mode)  # Pass mode to Player

    # Bind key events to the Player instance methods
    root.bind('<KeyPress>', player.on_key_press)
    root.bind('<KeyRelease>', player.on_key_release)
    canvas.bind('<Motion>', player.on_mouse_motion)

    # Spawn enemies around the player
    spawn_enemies(mode, player.x, player.y)

    # Start the movement loop
    player.move()
    update_enemies()

def spawn_enemies(mode, player_x, player_y):
    global enemies
    enemy_types = [BasicDrone, FastScout, ArmoredTank, FighterJet, CamouflagedStealth, SuicideBomber, EliteGuardian, SwarmDrone]
    
    # Spawn enemies in a random position around the player
    for _ in range(1):  # Number of enemies
        enemy_type = random.choice(enemy_types)
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(100, 300)  # Random distance from the player
        x = player_x + distance * math.cos(angle)
        y = player_y + distance * math.sin(angle)
        
        enemy = enemy_type(canvas, x, y, player_x, player_y)
        enemies.append(enemy)

def update_enemies():
    global enemies
    for enemy in enemies:
        if not enemy.is_out_of_bounds():
            enemy.move()
        else:
            enemies.remove(enemy)
    
    # Schedule the next update
    canvas.after(50, update_enemies)

# Create the home screen
create_home_screen(canvas)

# Run the main loop
root.mainloop()
