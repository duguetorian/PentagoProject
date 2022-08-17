import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def check_move_complete(move):
    for step in move:
        if step is None:
            return False
    return True


def reset_move(move, window):
    if move[0] is not None:
        window[(*move[0], 0)](button_color="grey")
    if move[1] is not None:
        window[(*move[1], 1)](button_color="grey")
    if move[2] is not None:
        window[move[2]](button_color="grey")
    move = [None, None, None]
    window["Play the move"](disabled=True)
    return (move, window)


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


# Create the layout for the first step
def generate_layout():
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
        [sg.Column([[sg.Canvas(key="board", size=(1, 1))]], justification="center")],
        [
            sg.Column(marbles, key="-1-STEP-", justification="center"),
            sg.Column(boards, key="-2-STEP-", justification="center"),
            sg.Column(direction, key="-3-STEP-", justification="center"),
        ],
        [
            sg.Column(commands, key="-4-STEP-", justification="right"),
        ],
    ]
