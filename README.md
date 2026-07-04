# minesweeper
This project is my final work for the Introduction to Programming course at university. It is a classic Minesweeper game with a graphical user interface, built with Python using the course's provided `haravasto` library (based on Pyglet).

<img width="608" height="741" alt="image" src="https://github.com/user-attachments/assets/da294ce9-4860-4ffe-be69-8e438f29067b" />



## Features

* **Custom game board:** You can choose the width (5–35) and height (5–20) of the board, as well as the number of mines.
* **Flood fill:** Clicking an empty square automatically opens all connected safe squares around it.
* **Flagging:** Right-click to place or remove flags on squares where you suspect a mine is hidden.
* **Game tracking:** The game measures how much time you spend and counts how many clicks you make during a game.
* **Statistics:** All game results (win/loss, duration, clicks, board size, date) are saved to a JSON file. You can browse your previous games directly from the main menu (shows 5 results per page).

## File Structure

* `minesweeper.py` – The main Python script that contains the game logic, UI events, and statistics handling.
* `haravasto.py` – A helper graphics library provided by the course (handles window creation, drawing, and mouse clicks).
* `icons/` – Folder containing all the game sprites and images (tiles, numbers, mine, flag).
* `statistics.json` – A file created automatically to store played game history.

## How to Run the Game

### Requirements
Make sure you have **Python 3** installed, along with the **Pyglet** library:
```bash
pip install pyglet
```

### Starting the game
Open your terminal in the project folder and run the program by giving a file name for the statistics as an argument:

```bash
python minesweeper.py statistics.json
```
(Note: If you run the command without the filename argument, the program will print usage instructions.)

### How to Play
When the game starts, choose an option from the menu:

A = Start a new game

T = View statistics

L = Quit the game

If you start a new game, enter your desired board size and mine count.

### Controls during the game:

Left click: Open a square.

Right click: Place or remove a flag.

You win the game when you have opened all safe squares without hitting any mines!
