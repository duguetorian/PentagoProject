import PySimpleGUI as sg

marbles_selection = [(row, col, 0) for row in range(6) for col in range(6)]
board_selection = [(row, col, 1) for row in range(2) for col in range(2)]


def check_move_incomplete(move):
    for step in move:
        if step is None:
            return True
    return False


player = 1
move = [None, None, None]

# Create the layout for the first step
marbles = [[sg.Text("Place your marble")]]

for row in range(6):
    new_row = []
    for column in range(6):
        new_row.append(
            sg.Button(size=(2, 1), key=(row, column, 0), button_color="grey")
        )
    marbles.append(new_row)

board = [[sg.Text("Choose which board to turn")]]

for row in range(2):
    new_row = []
    for col in range(2):
        new_row.append(sg.Button(size=(6, 3), key=(row, col, 1), button_color="grey"))
    board.append(new_row)

direction = [
    [sg.Text("Choose a rotation direction")],
    [
        sg.Button("<--", key=1, button_color="grey"),
        sg.Button("-->", key=-1, button_color="grey"),
    ],
]

commands = [
    [
        sg.Button("Cancel"),
        sg.Button("Play the move", disabled=check_move_incomplete(move)),
    ]
]

layout = [
    [sg.Column(marbles, key="-1-STEP-")],
    [sg.Column(board, key="-2-STEP-")],
    [sg.Column(direction, key="-3-STEP-")],
    [sg.Column(commands, key="-4-STEP-")],
]
# Create the window
window = sg.Window("Pentago", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window
    if event == sg.WIN_CLOSED:
        break

    if event == "Cancel":
        if move[0] is not None:
            window[(*move[0], 0)](button_color="grey")
        if move[1] is not None:
            window[(*move[1], 1)](button_color="grey")
        if move[2] is not None:
            window[move[2]](button_color="grey")
        move = [None, None, None]

    if event in marbles_selection:
        if move[0] is not None:
            window[(*move[0], 0)](button_color="grey")
        move[0] = event[slice(2)]
        print(move)
        window[event](button_color="black" if player == 1 else "white")

    if event in board_selection:
        if move[1] is not None:
            window[(*move[1], 1)](button_color="grey")
        move[1] = event[slice(2)]
        print(move)
        window[event](button_color="blue")

    if type(event) == int:
        if move[2] is not None:
            window[move[2]](button_color="grey")
        move[2] = event
        print(move)
        window[event](button_color="blue")

window.close()
