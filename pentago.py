import numpy as np
from IPython.display import clear_output


def turn(matrix, sens):
    """
    tourne une matrice de 90 degré dans le
    sens direct (sens=1) ou indirect (sens=-1)
    """
    if sens == 1:
        return np.flip(matrix.T, axis=1)
    else:
        return np.flip(matrix.T, axis=0)


class pentago:
    def __init__(self, plot_grid=True):
        """
        creer la table initiale
        """
        self.table = np.zeros(36).reshape(2, 2, 3, 3)
        self.winner = None
        self.plot_grid = plot_grid

    def play(self, player, position, flip, sens):
        """
        position représente la position de la bille placée,
        flip la position du tableau à pivoter
        dir le sens dans lequel on pivote
        """
        pos = (position[1] // 3, position[0] // 3, position[0] % 3, position[1] % 3)
        if self.table[pos] == 0.0:
            self.table[pos] = player.number
        else:
            raise ValueError(
                f"Wrong position : coordinate {position, pos} has value {self.table[pos]}"
            )

        self.table[flip] = turn(self.table[flip], sens)
        self.check_winner()

    def check_winner(self):
        table = np.concatenate(
            (
                np.concatenate((self.table[0, 0], self.table[0, 1])),
                np.concatenate((self.table[1, 0], self.table[1, 1])),
            ),
            axis=1,
        )

        if self.plot_grid:
            clear_output()
            print(table)

        winners = []

        if 0 not in table:
            if self.plot_grid:
                print("No winners")
            self.winner = "both"

        if not self.winner:
            for i in range(6):
                for j in range(2):
                    if list(table[i, j : j + 5]) == [1 for i in range(5)]:
                        winners.append(1)
                    elif list(table[i, j : j + 5]) == [2 for i in range(5)]:
                        winners.append(2)

            for j in range(6):
                for i in range(2):
                    if list(table[i : i + 5, j]) == [1 for i in range(5)]:
                        winners.append(1)
                    elif list(table[i : i + 5, j]) == [2 for i in range(5)]:
                        winners.append(2)
            for j in range(2):
                for i in range(2):
                    if [table[k + i, k + j] for k in range(5)] == [1 for i in range(5)]:
                        winners.append(1)
                    elif [table[k + i, k + j] for k in range(5)] == [
                        2 for i in range(5)
                    ]:
                        winners.append(2)

            if 1 in winners and 2 not in winners:
                if self.plot_grid:
                    print("Player 1 wins")
                self.winner = 1

            elif 1 not in winners and 2 in winners:
                if self.plot_grid:
                    print("Player 2 wins")
                self.winner = 2

            elif 1 in winners and 1 not in winners:
                if self.plot_grid:
                    print("No winners")
                self.winner = "both"
