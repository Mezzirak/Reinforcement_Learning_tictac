import numpy as np

class TicTacToe:
    def __init__(self):
        self.reset()

    def reset(self):
        "Reset the board to empty."
        self.board = np.zeros((3, 3), dtype=int)
        self.done = False
        self.winner = None
        return self._get_state()

    def _get_state(self):
        "Encode the board as a tuple for Q-table indexing."
        return tuple(self.board.flatten())

    def get_valid_actions(self):
        "Return list of available positions (0-8)."
        return [i for i in range(9) if self.board.flatten()[i] == 0]

    def step(self, action, player=1):
        "Place a marker for the player and return next_state, reward, done."
        if self.done:
            raise ValueError("Game is over. Please reset.")
        if self.board.flatten()[action] != 0:
            return self._get_state(), -0.5, True

        row, col = divmod(action, 3)
        self.board[row, col] = player

        reward = 0
        if self._check_winner(player):
            reward = 1
            self.done = True
            self.winner = player
        elif len(self.get_valid_actions()) == 0:
            reward = -0.1  # Penalty for a draw
            self.done = True

        return self._get_state(), reward, self.done

    def _check_winner(self, player):
        "Check if the player has won."
        for i in range(3):
            if all(self.board[i, :] == player) or all(self.board[:, i] == player):
                return True
        if self.board[0,0] == self.board[1,1] == self.board[2,2] == player:
            return True
        if self.board[0,2] == self.board[1,1] == self.board[2,0] == player:
            return True
        return False

    def render(self):
        "Print the board."
        symbols = {0: " ", 1: "X", -1: "O"}
        for row in self.board:
            print("|".join([symbols[cell] for cell in row]))
            print("-"*5)
