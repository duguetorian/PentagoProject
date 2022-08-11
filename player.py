import numpy as np


class player:
    def __init__(self, number):
        if number == 1 or number == 2:
            self.number = number
        else:
            raise ValueError("Invalid number")

    def play(self, position, flip, sens, game):
        game.play(self, position, flip, sens)

    def random_play(self, game):
        """
        plays a random case, flips a random case in a random direction
        """
        state = True
        while state:
            position = np.random.randint(0, 6, size=2)
            pos = (position[1] // 3, position[0] // 3, position[0] % 3, position[1] % 3)
            flip = tuple(np.random.randint(0, 2, size=2))
            sens = [1, -1][int(np.random.randint(0, 2, size=1))]
            if game.table[pos] == 0:
                self.play(position, flip, sens, game)
                state = False

    def smart_play(self, game):
        """
        trouve la plus longue chaine de pièces et la complète,
        tourne la table de façon à ne pas détruire sa chaine la plus longue
        """

        table = np.concatenate(
            (
                np.concatenate((game.table[0, 0], game.table[0, 1])),
                np.concatenate((game.table[1, 0], game.table[1, 1])),
            ),
            axis=1,
        )

        pieces_coor = [
            (np.where(table == self.number)[0][i], np.where(table == self.number)[1][i])
            for i in range(np.size(np.where(table == self.number)) // 2)
        ]
        zeros_coor = [
            (np.where(table == 0)[0][i], np.where(table == 0)[1][i])
            for i in range(np.size(np.where(table == 0)) // 2)
        ]

        max_length = 0
        max_length_coor = None
        flip = (0, 0)

        for x in pieces_coor:

            # vertical chains
            length = 0
            while (x[0], x[1] + length) in pieces_coor:
                length += 1

            if length > max_length:

                if x[1] + length <= 5:
                    max_length_coor = (x[0], x[1] + length)
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                else:
                    max_length_coor = (x[0], x[1] - 1)
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                if max_length_coor:
                    max_length = length
                    flip = (
                        [0, 1][max_length_coor[0] // 3 - 1],
                        max_length_coor[1] // 3,
                    )

            # horizontal chains
            length = 0
            while (x[0] + length, x[1]) in pieces_coor:
                length += 1

            if length > max_length:

                if x[0] + length <= 5:
                    max_length_coor = (x[0] + length, x[1])
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                else:
                    max_length_coor = (x[0] - 1, x[1])
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                if max_length_coor:
                    max_length = length
                    flip = (
                        max_length_coor[0] // 3,
                        [0, 1][max_length_coor[1] // 3 - 1],
                    )

            # diagonal chains
            length = 0
            while (x[0] + length, x[1] + length) in pieces_coor:
                length += 1

            if length > max_length:

                if x[0] + length <= 5 and x[1] + length <= 5:
                    max_length_coor = (x[0] + length, x[1] + length)
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                elif x[0] + length <= 5 and x[1] + length > 5:
                    max_length_coor = (x[0] + length, x[1] - 1)
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                elif x[0] + length > 5 and x[1] + length <= 5:
                    max_length_coor = (x[0] - 1, x[1] + length)
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                else:
                    max_length_coor = (x[0] - 1, x[1] - 1)
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                if max_length_coor:
                    max_length = length
                    flip = (
                        [0, 1][max_length_coor[0] // 3 - 1],
                        [0, 1][max_length_coor[1] // 3 - 1],
                    )
        if max_length_coor:

            self.play(max_length_coor, flip, 1, game)

        else:

            self.random_play(game)  # plays randomly if there are no chains
