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
    
    
    
    def is_valid_move(self, selected, new_position):
        selected_x, selected_y = selected
        new_x, new_y = new_position
        # Check if the move is horizontal or vertical by one square only
        return (selected_x == new_x and abs(selected_y - new_y) == 1) or \
               (selected_y == new_y and abs(selected_x - new_x) == 1)

    def on_click(self, x, y):
        # Si hay un cuadrado seleccionado y el nuevo clic es un cuadrado vacío
        if self.board[x][y] == 0 and self.selected:
            # Última posición seleccionada en el camino actual
            last_x, last_y = self.path[-1] if self.path else self.selected
            if self.is_valid_move((last_x, last_y), (x, y)):
                self.path.append((x, y))
                self.buttons[x][y].config(bg="gray")
        # Si el nuevo clic es en un cuadrado con número y no hay nada seleccionado
        elif self.board[x][y] != 0:
            if not self.selected:
                # Inicio de un nuevo camino
                self.selected = (x, y)
                self.path = [(x, y)]
                self.buttons[x][y].config(bg="green")
            else:
                # Intento de completar un camino
                if self.board[x][y] == self.board[self.selected[0]][self.selected[1]] and (x, y) != self.selected:
                    last_x, last_y = self.path[-1]
                    if self.is_valid_move((last_x, last_y), (x, y)):
                        # Final del camino
                        self.path.append((x, y))
                        for px, py in self.path:
                            self.board[px][py] = self.board[self.selected[0]][self.selected[1]]
                            self.buttons[px][py].config(bg="yellow", text=self.board[px][py])
                        self.selected = None
                        self.path = []
                        self.check_game_completion()
        # Si el movimiento no es válido,

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