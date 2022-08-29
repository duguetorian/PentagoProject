import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from board_generation import generate_figure, matrix_conversion
from pentago import pentago
from player import player


class game_interface:
    def __init__(
        self,
        player1_type,
        player2_type,
        player1_name="Player 1",
        player2_name="Player 2",
        player1_lvl=None,
        player2_lvl=None,
        nb_games=None,
    ):
        # List of all marbles and boards selection used to discriminate events
        self.marbles_selection = [(row, col, 0) for row in range(6) for col in range(6)]
        self.board_selection = [(row, col, 1) for row in range(2) for col in range(2)]

        # Set up the players
        self.player1 = player(1, player1_name, player1_type, player1_lvl)
        self.player2 = player(2, player2_name, player2_type, player2_lvl)
        # Get the number of games to be played when it is AI vs AI
        self.nb_games = int(nb_games)

        # Set up the game and initialize the first move
        self.game = pentago(plot_grid=False)
        self.move = [None, None, None]
        self.active_player = self.player1

        # Set up the interface
        self.window = None
        self.fig_plt = None
        self.fig_agg = None

        # Choose which type of game to be played
        if self.player1.type == self.player2.type == "AI":
            self.start_games()
        else:
            self.start_game()

    # Reset the game but notthe interface
    def reset_game(self):
        self.player1 = player(1, self.player1.name, self.player1.type, self.player1.lvl)
        self.player2 = player(2, self.player2.name, self.player2.type, self.player2.lvl)
        self.game = pentago(plot_grid=False)

    # Generate the layout of the game
    def generate_layout(self):
        marbles = [[sg.Text("Place your marble")]]

        for row in range(6):
            new_row = []
            for column in range(6):
                new_row.append(
                    sg.Button(
                        size=(2, 1),
                        key=(row, column, 0),
                        button_color="grey",
                        disabled_button_color="darkred",
                    )
                )
            marbles.append(new_row)

        boards = [[sg.Text("Choose which board to turn")]]

        for row in range(2):
            new_row = []
            for col in range(2):
                new_row.append(
                    sg.Button(size=(6, 3), key=(col, row, 1), button_color="grey")
                )
            boards.append(new_row)

        direction = [
            [sg.Text("Choose a rotation direction")],
            [
                sg.Button("⟲", key=-1, button_color="grey", font=("", 40), size=(1, 1)),
                sg.Button("⟳", key=1, button_color="grey", font=("", 40)),
            ],
        ]

        commands = [
            [
                sg.Button("Cancel"),
                sg.Button("Play the move", disabled=True),
            ]
        ]

        return [
            [
                sg.Column(
                    [[sg.Canvas(key="board", size=(1, 1))]], justification="center"
                )
            ],
            [
                sg.Column(marbles, key="-1-STEP-", justification="center"),
                sg.Column(boards, key="-2-STEP-", justification="center"),
                sg.Column(direction, key="-3-STEP-", justification="center"),
            ],
            [
                sg.Column(commands, key="-4-STEP-", justification="right"),
            ],
        ]

    # Draw the board with matplotlib
    def draw_figure(self, canvas_name):
        figure_canvas_agg = FigureCanvasTkAgg(
            self.fig_plt, self.window[canvas_name].TKCanvas
        )
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_canvas_agg

    # Check if the move is complete in order to allow to play it
    def check_move_complete(self):
        for step in self.move:
            if step is None:
                return False
        return True

    # Reset the move and the interface of the move
    def reset_move(self):
        if self.move[0] is not None:
            self.window[(*self.move[0], 0)](button_color="grey")
        if self.move[1] is not None:
            self.window[(*self.move[1], 1)](button_color="grey")
        if self.move[2] is not None:
            self.window[self.move[2]](button_color="grey")
        self.move = [None, None, None]
        self.window["Play the move"](disabled=True)

    # Disable the buttons of the marbles' slots already taken
    def disable_marbles_buttons(self):
        table = matrix_conversion(self.game.table)
        for i in range(6):
            for j in range(6):
                if table[i, j] != 0:
                    self.window[(i, j, 0)](disabled=True)
                else:
                    self.window[(i, j, 0)](disabled=False)

    # Update the matplotlib figure with the new datas of the game
    def update_board(self):
        self.fig_agg.get_tk_widget().forget()
        self.fig_plt = generate_figure(self.game.table)
        self.fig_agg = self.draw_figure("board")
        self.active_player = (
            self.player2 if self.active_player == self.player1 else self.player1
        )
        self.reset_move()
        self.game.check_winner()
        self.disable_marbles_buttons()

    # Start the game between players and AIs (only not AI vs AI)
    def start_game(self):
        layout = self.generate_layout()
        self.window = sg.Window("Pentago", layout, finalize=True, resizable=True)
        self.fig_plt = generate_figure(self.game.table)
        self.fig_agg = self.draw_figure("board")

        while True:
            if self.active_player.type == "AI":
                if self.active_player.lvl == "Easy":
                    self.active_player.random_play(self.game)
                else:
                    self.active_player.smart_play(self.game)
                self.update_board()

            event, values = self.window.read()

            # End program if user closes window
            if event == sg.WIN_CLOSED:
                break

            if event == "Cancel":
                self.reset_move()

            if event in self.marbles_selection:
                if self.move[0] is not None:
                    self.window[(*self.move[0], 0)](button_color="grey")
                self.move[0] = event[slice(2)]
                self.window[event](button_color="blue")

            if event in self.board_selection:
                if self.move[1] is not None:
                    self.window[(*self.move[1], 1)](button_color="grey")
                self.move[1] = event[slice(2)]
                self.window[event](button_color="blue")

            if type(event) == int:
                if self.move[2] is not None:
                    self.window[self.move[2]](button_color="grey")
                self.move[2] = event
                self.window[event](button_color="blue")

            if self.check_move_complete():
                self.window["Play the move"](disabled=False)

            if event == "Play the move":
                self.game.play(self.active_player, *self.move)
                self.update_board()

                if self.game.winner:
                    winner = self.player1 if self.game.winner == 1 else self.player2
                    sg.Popup(f"{winner.name} has won", title="Game ended")
                    break

        self.window.close()

    # Start multiple games in a row of AI vs AI
    def start_games(self):
        layout = [
            [sg.Text(f"Wins repartition for {self.nb_games} games")],
            [sg.Canvas(key="graph")],
        ]
        self.window = sg.Window("Pentago", layout, finalize=True, resizable=True)

        player1_wins = []
        player2_wins = []

        for i in tqdm(range(self.nb_games)):
            self.reset_game()
            while not self.game.winner:
                self.player1.random_play(
                    self.game
                ) if self.player1.lvl == "Easy" else self.player1.smart_play(self.game)
                if not self.game.winner:
                    self.player2.random_play(
                        self.game
                    ) if self.player2.lvl == "Easy" else self.player2.smart_play(
                        self.game
                    )

            if self.game.winner == 1:
                player1_wins.append(1)
                player2_wins.append(0)
            elif self.game.winner == 2:
                player1_wins.append(0)
                player2_wins.append(1)
            else:
                player1_wins.append(0)
                player2_wins.append(0)

        player1_wins = np.array(player1_wins)
        player2_wins = np.array(player2_wins)

        self.fig_plt = plt.figure(figsize=(10, 5))
        plt.plot(player1_wins.cumsum())
        plt.plot(player2_wins.cumsum())
        plt.legend(
            [
                f"Player 1 wins in {self.player1.lvl} mode",
                f"Player 2 wins in {self.player2.lvl} mode",
            ]
        )
        self.fig_agg = self.draw_figure("graph")
