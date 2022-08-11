import PySimpleGUI as sg

from interface import generate_layout, draw_figure, reset_move, check_move_complete
from board_generation import generate_figure
from pentago import pentago
from player import player

marbles_selection = [(row, col, 0) for row in range(6) for col in range(6)]
board_selection = [(row, col, 1) for row in range(2) for col in range(2)]

VARS = {
    "player1": False,
    "player2": False,
    "game": False,
    "move": False,
    "window": False,
    "fig_plt": False,
    "fig_agg": False,
}

# Set up the game
VARS["player1"], VARS["player2"] = player(1), player(2)
VARS["game"] = pentago(plot_grid=False)
VARS["move"] = [None, None, None]
VARS["active_player"] = VARS["player1"]

# Set up interface values
layout = generate_layout()
VARS["window"] = sg.Window("Pentago", layout, finalize=True, resizable=True)
VARS["fig_plt"] = generate_figure(VARS["game"].table)
VARS["fig_agg"] = draw_figure(VARS["window"]["board"].TKCanvas, VARS["fig_plt"])


# Create an event loop
while True:
    event, values = VARS["window"].read()

    # End program if user closes window
    if event == sg.WIN_CLOSED:
        break

    if event == "Cancel":
        VARS["move"], VARS["window"] = reset_move(VARS["move"], VARS["window"])

    if event in marbles_selection:
        if VARS["move"][0] is not None:
            VARS["window"][(*VARS["move"][0], 0)](button_color="grey")
        VARS["move"][0] = event[slice(2)]
        VARS["window"][event](button_color="blue")

    if event in board_selection:
        if VARS["move"][1] is not None:
            VARS["window"][(*VARS["move"][1], 1)](button_color="grey")
        VARS["move"][1] = event[slice(2)]
        VARS["window"][event](button_color="blue")

    if type(event) == int:
        if VARS["move"][2] is not None:
            VARS["window"][VARS["move"][2]](button_color="grey")
        VARS["move"][2] = event
        VARS["window"][event](button_color="blue")

    if check_move_complete(VARS["move"]):
        VARS["window"]["Play the move"](disabled=False)

    if event == "Play the move":
        VARS["game"].play(VARS["active_player"], *VARS["move"])
        VARS["fig_agg"].get_tk_widget().forget()
        VARS["fig_plt"] = generate_figure(VARS["game"].table)
        VARS["fig_agg"] = draw_figure(VARS["window"]["board"].TKCanvas, VARS["fig_plt"])
        VARS["active_player"] = (
            VARS["player2"]
            if VARS["active_player"] == VARS["player1"]
            else VARS["player1"]
        )
        VARS["move"], VARS["window"] = reset_move(VARS["move"], VARS["window"])
        VARS["game"].check_winner()
        if VARS["game"].winner:
            winner = VARS["game"].winner
            sg.Popup(f"Player {winner} has won")

VARS["window"].close()

# random_play_wins = []
# smart_play_wins = []

# for i in tqdm(range(70)):
    
#     player1, player2 = player(1), player(2)
#     game = pentago(plot_grid=False)
#     while not game.winner:
#         player1.random_play(game)
#         if not game.winner:
#             player2.smart_play(game)
                        
#     if game.winner == 1:
#         random_play_wins.append(1)
#         smart_play_wins.append(0)
#     elif game.winner == 2:
#         random_play_wins.append(0)
#         smart_play_wins.append(1)
#     else:
#         random_play_wins.append(0)
#         smart_play_wins.append(0)
    
        
# random_play_wins = np.array(random_play_wins)
# smart_play_wins = np.array(smart_play_wins)

# plt.figure(figsize=(10, 5))
# plt.plot(random_play_wins.cumsum())
# plt.plot(smart_play_wins.cumsum())
# plt.legend(['random play', 'smart play'])
# plt.show()