# AstroBlasters

**AstroBlasters** is an exciting 2D space shooter game developed using Python's Tkinter library. The game features different modes, player movement, shooting mechanics, and a cooldown system for firing lasers. 

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [License](#license)

## Features

- **Game Modes**: Includes different game modes such as "Orbital Defense" and placeholders for additional modes.
- **Player Controls**: Use the `W`, `A`, `S`, `D` keys to move the player, and the left mouse button to shoot lasers.
- **Laser Mechanics**: Lasers can bounce off the canvas edges (except in "Orbital Defense" mode) and have a cooldown period between shots.
- **Cooldown System**: A visual cooldown bar shows the remaining time before the player can shoot again.

## Installation

1. Ensure you have Python installed on your system.
2. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/AstroBlasters.git
   ```
3. Navigate into the project directory:
   ```bash
   cd AstroBlasters
   ```
4. Install any dependencies (if needed). The current project does not require additional Python packages beyond the standard library.

## Usage

1. Run the main game file:
   ```bash
   python pythonGame.py
   ```
2. The game will display a home screen with a "Start" button. Click it to go to the mode selection screen.
3. Choose a game mode and start playing!

## File Structure

- **`pythonGame.py`**: The main script that initializes the Tkinter window, sets up the game canvas, and manages transitions between screens.
- **`player.py`**: Defines the `Player` class, including player movement, shooting mechanics, and cooldown bar functionality.
- **`laser.py`**: Defines the `Laser` class, including laser creation, movement, and bouncing behavior.

### Code Overview

- **`pythonGame.py`**: 
  - Initializes the game window and canvas.
  - Defines functions for creating the home screen and mode selection screen.
  - Handles transitions between screens and initializes the player.

- **`player.py`**: 
  - Contains the `Player` class with methods for creating and moving the player, shooting lasers, and updating the cooldown bar.
  - Binds mouse and keyboard events to player actions.

- **`laser.py`**: 
  - Contains the `Laser` class with methods for creating and moving lasers, handling bouncing, and interacting with canvas boundaries.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
