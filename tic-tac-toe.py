import tkinter as tk
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("800x600")

        self.player_options = ["X", "O"]
        self.current_player = "X"
        self.difficulty_levels = ["Easy", "Medium", "Hard"]
        self.current_difficulty = "Easy"

        self.board = [" " for _ in range(9)]

        # Create buttons for the Tic-Tac-Toe grid
        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = tk.Button(root, text=" ", font=("Helvetica", 24), width=6, height=3,
                                   command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j)
                self.buttons.append(button)

        # Create the player options menu
        self.player_var = tk.StringVar(root)
        self.player_var.set(self.player_options[0])
        player_menu = tk.OptionMenu(root, self.player_var, *self.player_options)
        player_menu.grid(row=0, column=4, columnspan=3, padx=10, pady=10)

        # Create the difficulty level menu
        self.difficulty_var = tk.StringVar(root)
        self.difficulty_var.set(self.difficulty_levels[0])
        difficulty_menu = tk.OptionMenu(root, self.difficulty_var, *self.difficulty_levels)
        difficulty_menu.grid(row=1, column=4, columnspan=3, padx=10, pady=10)

        # Create the start button
        start_button = tk.Button(root, text="Start", font=("Helvetica", 16), command=self.start_game)
        start_button.grid(row=2, column=4, columnspan=3, padx=10, pady=10)

        # Create the reset button
        reset_button = tk.Button(root, text="Reset", font=("Helvetica", 16), command=self.reset_game)
        reset_button.grid(row=3, column=4, columnspan=3, padx=10, pady=10)

        # Create a label to display the winner
        self.winner_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.winner_label.grid(row=4, column=4, columnspan=3, padx=10, pady=10)

    def start_game(self):
        self.current_player = self.player_var.get()
        self.current_difficulty = self.difficulty_var.get()
        self.reset_game()

    def make_move(self, row, col):
        index = 3 * row + col
        if self.board[index] == " " and not self.check_winner():
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            winner = self.check_winner()
            if winner:
                self.winner_label.config(text=f"{winner} wins!")
            elif " " not in self.board:
                self.winner_label.config(text="It's a draw!")
            else:
                self.switch_player()
                if self.current_player == "O" and not self.check_winner():
                    self.make_ai_move()

    def switch_player(self):
        self.current_player = "X" if self.current_player == "O" else "O"

    def make_ai_move(self):
        if " " in self.board:
            index = self.get_best_move()
            self.board[index] = "O"
            self.buttons[index].config(text="O")
            winner = self.check_winner()
            if winner:
                self.winner_label.config(text=f"{winner} wins!")
            elif " " not in self.board:
                self.winner_label.config(text="It's a draw!")
            else:
                self.switch_player()

    def get_best_move(self):
        if self.current_difficulty == "Easy":
            # Easy level: Random move
            return random.choice([i for i, value in enumerate(self.board) if value == " "])
        elif self.current_difficulty == "Medium":
            # Medium level: Random move for now (you can implement a better strategy)
            return random.choice([i for i, value in enumerate(self.board) if value == " "])
        else:
            # Hard level: Minimax algorithm
            best_score = float('-inf')
            best_move = None
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "O"
                    score = self.minimax(self.board, 0, False)
                    self.board[i] = " "
                    if score > best_score:
                        best_score = score
                        best_move = i
            return best_move

    def minimax(self, board, depth, is_maximizing):
        scores = {"X": -1, "O": 1, "draw": 0}

        winner = self.check_winner(board)
        if winner:
            return scores[winner]

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def reset_game(self):
        self.current_player = self.player_var.get()
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ")
        self.winner_label.config(text="")

    def check_winner(self, board=None):
        board = board or self.board
        # Check rows, columns, and diagonals for a winner
        for i in range(3):
            if board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] != " ":
                return board[i * 3]
            if board[i] == board[i + 3] == board[i + 6] != " ":
                return board[i]
        if board[0] == board[4] == board[8] != " ":
            return board[0]
        if board[2] == board[4] == board[6] != " ":
            return board[2]
        if " " not in board:
            return "draw"
        return None

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
