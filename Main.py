import tkinter as tk
from tkinter import messagebox


class NumberLinkGame:
    def __init__(self, board):
        self.board = board
        self.root = tk.Tk()
        self.root.title("NumberLink/FreeFlow Game")
        self.selected = None
        self.path = []

        # Display the board
        self.buttons = [[None for _ in row] for row in board]
        for i in range(len(board)):
            for j in range(len(board[0])):
                text = board[i][j] if board[i][j] != 0 else ""
                btn = tk.Button(self.root, text=str(text), width=5, height=2)
                btn.grid(row=i, column=j)
                btn.bind("<Button-1>", lambda event, x=i, y=j: self.on_click(x, y))
                btn.bind("<Button-3>", lambda event, x=i, y=j: self.undo(x, y))
                self.buttons[i][j] = btn

    def on_click(self, x, y):
        if self.board[x][y] == 0 and self.selected:
            # Mark path
            self.path.append((x, y))
            self.buttons[x][y].config(bg="gray")
        elif self.board[x][y] != 0:
            if not self.selected:
                self.selected = (x, y)
                self.path = [(x, y)]
                self.buttons[x][y].config(bg="green")
            else:
                # Check if it's the matching number
                if self.board[x][y] == self.board[self.selected[0]][self.selected[1]] and (x, y) != self.selected:
                    self.path.append((x, y))
                    for px, py in self.path:
                        self.board[px][py] = self.board[self.selected[0]][self.selected[1]]
                        self.buttons[px][py].config(bg="yellow", text=self.board[px][py])
                    self.selected = None
                    self.path = []
                    self.check_game_completion()
                else:
                    # Reset path
                    for px, py in self.path:
                        self.buttons[px][py].config(bg="white")
                    self.selected = (x, y)
                    self.path = [(x, y)]
                    self.buttons[x][y].config(bg="green")

    def undo(self, x, y):
        # If the undone cell is part of an existing path (not the current path), clear the entire path but preserve start and end numbers
        number = self.board[x][y]
        if number != 0 and (
                (not self.selected) or (self.selected and self.board[self.selected[0]][self.selected[1]] != number)):
            start, end = [], []
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] == number:
                        if not start:
                            start = [i, j]
                        else:
                            end = [i, j]
                        self.board[i][j] = 0
                        self.buttons[i][j].config(bg="white", text="")

            self.board[start[0]][start[1]] = number
            self.buttons[start[0]][start[1]].config(bg="white", text=number)
            self.board[end[0]][end[1]] = number
            self.buttons[end[0]][end[1]].config(bg="white", text=number)
            return

        # Allow undo only for the cells in the current path
        if (x, y) in self.path:
            # If the undone cell is the starting cell of the current path, clear the entire path but don't erase the starting number
            if number != 0 and (x, y) == self.path[0]:
                for px, py in self.path[1:]:
                    self.board[px][py] = 0
                    self.buttons[px][py].config(bg="white", text="")
                self.selected = None
                self.path = []
            elif number == 0:
                self.path.remove((x, y))
                self.buttons[x][y].config(bg="white", text="")
                self.board[x][y] = 0

    def check_game_completion(self):
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return
        messagebox.showinfo("Congratulations!", "You have completed the game!")

    def run(self):
        self.root.mainloop()


def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        n, m = map(int, lines[0].split(','))
        board = [[0 for _ in range(m)] for _ in range(n)]
        for line in lines[1:]:
            x, y, value = map(int, line.split(','))
            board[x - 1][y - 1]
            board[x-1][y-1] = value
    return board

if __name__ == "__main__":
    board = read_input_file("juego.txt")  # Replace with the actual path to your input file
    game = NumberLinkGame(board)
    game.run()