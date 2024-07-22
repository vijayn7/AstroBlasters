# AstroBlasters

AstroBlasters is a space-themed game built with Python and Tkinter. Players navigate through various game modes, shooting enemies and dodging obstacles in a dynamic, star-filled environment.

## Features

- **Starry Background**: Animated star field for a visually appealing background.
- **Game Modes**: Multiple game modes with unique mechanics.
- **Enemies**: Various enemy types with different movement patterns and behaviors.
- **Pause Menu**: Functionality to pause the game and return to the main menu.

## Getting Started

### Prerequisites

- Python 3.x
- Tkinter (usually comes with Python installation)
- Docker (optional, for containerization)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/astrobusters.git
   cd astrobusters
   ```

2. **Install Dependencies:**

   It is recommended to use a virtual environment. Install dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Game:**

   ```bash
   python game/main.py
   ```

## Dockerization

To build and run the Docker container for AstroBlasters, follow these steps:

1. **Build the Docker Image:**

   ```bash
   docker build -t astrobusters .
   ```

2. **Run the Docker Container:**

   ```bash
   docker run -p 4000:80 astrobusters
   ```

   The game will be accessible at `http://localhost:4000` inside the container.

### Docker Compose (Optional)

If you have multiple services or dependencies, you can use Docker Compose. Create a `docker-compose.yml` file and use the following commands:

1. **Build and Start Services:**

   ```bash
   docker-compose up --build
   ```

## Unit Testing

Unit tests are located in the `tests` directory. To run the tests:

1. **Install Test Dependencies:**

   ```bash
   pip install -r requirements-test.txt
   ```

2. **Run the Tests:**

   ```bash
   pytest
   ```

## Project Structure

- `game/`: Contains the game logic and main entry point.
  - `main.py`: Main script to start the game.
  - `player.py`: Defines the `Player` class.
  - `laser.py`: Defines the `Laser` class.
  - `enemy.py`: Defines enemy classes.
- `tests/`: Contains unit tests for the project.
  - `test_player.py`: Tests for the `Player` class.
  - `test_laser.py`: Tests for the `Laser` class.
  - `test_enemy.py`: Tests for enemy classes.
- `Dockerfile`: Docker configuration for containerizing the application.
- `docker-compose.yml`: Docker Compose configuration (if needed).
- `requirements.txt`: Python dependencies.
- `requirements-test.txt`: Test dependencies.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.

## Contact

For questions or comments, please reach out to [vijaynannapuraju@gmail.com](mailto:vijaynannapuraju@gmail.com).
