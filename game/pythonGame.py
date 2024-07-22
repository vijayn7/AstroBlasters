import math
import tkinter as tk
from game.player import Player
from game.enemy import BasicDrone, FastScout, ArmoredTank, FighterJet, CamouflagedStealth, SuicideBomber, EliteGuardian, SwarmDrone
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
stars = []  # List to hold star data for animation
paused = False  # Flag to track if the game is paused
pause_menu_items = []  # List to hold pause menu items

def create_star_field(canvas, num_stars=100):
    """Draws a starry background on the canvas."""
    global stars
    for _ in range(num_stars):
        x = random.randint(0, canvas_width)
        y = random.randint(0, canvas_height)
        size = random.randint(1, 3)  # Small variation in star size
        star = canvas.create_oval(x - size, y - size, x + size, y + size, fill="white", outline="white", tags="star")
        stars.append((star, size))

def animate_stars():
    """Animate the stars to create a moving background effect."""
    if not paused:  # Only animate if the game is not paused
        for star, size in stars:
            x0, y0, x1, y1 = canvas.coords(star)
            move_x = random.uniform(-0.5, 0.5)  # Small horizontal movement
            move_y = random.uniform(-0.5, 0.5)  # Small vertical movement

            canvas.move(star, move_x, move_y)

            # Check bounds and reset if necessary
            if x1 < 0 or x0 > canvas_width or y1 < 0 or y0 > canvas_height:
                new_x = random.randint(0, canvas_width)
                new_y = random.randint(0, canvas_height)
                canvas.coords(star, new_x - size, new_y - size, new_x + size, new_y + size)

        canvas.after(50, animate_stars)  # Repeat animation

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
    create_star_field(canvas)  # Recreate star field for mode selection
    create_mode_selection_screen(canvas)
    animate_stars()  # Start animating stars

def transition_to_game(mode):
    canvas.delete("all")  # Clear the mode selection screen
    create_star_field(canvas)  # Add starry background

    # Initialize the game elements based on selected mode
    player_size = 30
    player_x = canvas_width // 2
    player_y = canvas_height // 2
    player = Player(canvas, player_x, player_y, player_size, mode)  # Pass mode to Player

    # Bind key events to the Player instance methods
    root.bind('<KeyPress>', player.on_key_press)
    root.bind('<KeyRelease>', player.on_key_release)
    canvas.bind('<Motion>', player.on_mouse_motion)

    # Bind the Escape key to toggle the pause menu
    root.bind('<Escape>', toggle_pause)

    # Spawn enemies around the player
    spawn_enemies(mode, player.x, player.y)

    # Start the movement loop
    player.move()
    update_enemies()

def spawn_enemies(mode, player_x, player_y):
    global enemies
    enemy_types = [BasicDrone, FastScout, ArmoredTank, FighterJet, CamouflagedStealth, SuicideBomber, EliteGuardian, SwarmDrone]
    
    # Spawn enemies in a random position around the player
    for _ in range(5):  # Number of enemies
        enemy_type = random.choice(enemy_types)
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(100, 300)  # Random distance from the player
        x = player_x + distance * math.cos(angle)
        y = player_y + distance * math.sin(angle)
        
        enemy = enemy_type(canvas, x, y, player_x, player_y)
        enemies.append(enemy)

def update_enemies():
    global enemies
    if not paused:  # Only update enemies if the game is not paused
        for enemy in enemies:
            if not enemy.is_out_of_bounds():
                enemy.move()
            else:
                enemies.remove(enemy)
    
    # Schedule the next update
    canvas.after(50, update_enemies)

def toggle_pause(event=None):
    """Toggle the game's paused state and display the pause menu."""
    global paused
    paused = not paused

    if paused:
        show_pause_menu()
    else:
        hide_pause_menu()
        # Resume animations and updates
        animate_stars()
        update_enemies()

def show_pause_menu():
    """Display the pause menu."""
    global pause_menu_items
    pause_menu_items.append(canvas.create_rectangle(350, 300, 650, 500, fill="gray", stipple="gray50", tags="pause_menu"))
    pause_menu_items.append(canvas.create_text(500, 350, text="Paused", fill="white", font=("Helvetica", 24), tags="pause_menu"))
    
    resume_button = tk.Button(root, text="Resume", command=toggle_pause, font=("Helvetica", 18, "bold"), bg="#333", fg="white", relief="raised", padx=10, pady=5)
    resume_button_window = canvas.create_window(500, 400, window=resume_button, tags="pause_menu_button")
    pause_menu_items.append(resume_button_window)
    
    main_menu_button = tk.Button(root, text="Main Menu", command=transition_to_mode_selection, font=("Helvetica", 18, "bold"), bg="#333", fg="white", relief="raised", padx=10, pady=5)
    main_menu_button_window = canvas.create_window(500, 450, window=main_menu_button, tags="pause_menu_button")
    pause_menu_items.append(main_menu_button_window)

def hide_pause_menu():
    """Hide the pause menu."""
    global pause_menu_items
    for item in pause_menu_items:
        if isinstance(item, tk.Widget):
            item.destroy()  # Destroy button widget
        else:
            canvas.delete(item)  # Delete canvas items
    pause_menu_items.clear()

# Create the home screen and start star animation
create_star_field(canvas)  # Initial star field for home screen
create_home_screen(canvas)
animate_stars()  # Start animating stars

# Run the main loop
root.mainloop()
