import PySimpleGUI as sg

player_type = ["Player", "AI"]

AI_level = ["Beginner", "Intermediate", "Expert"]

layout = [
    [sg.Text("Set up the game: ")],
    [
        sg.Text("Player 1"),
        sg.Combo(player_type, key="P1", readonly=True, enable_events=True),
        sg.Input(key="P1 name", visible=False),
        sg.Combo(AI_level, default_value="Intermediate", key="P1 level", visible=False),
    ],
    [
        sg.Text("Player 2"),
        sg.Combo(player_type, key="P2", readonly=True, enable_events=True),
        sg.Input(key="P2 name", visible=False),
        sg.Combo(AI_level, default_value="Intermediate", key="P2 level", visible=False),
    ],
    [
        sg.Column(
            [[sg.Button("Quit"), sg.Button("Play", disabled=True)]],
            justification="right",
        )
    ],
]

window = sg.Window("Launcher", layout)

while True:
    event, value = window.read()
    if event == sg.WIN_CLOSED or event == "Quit":
        break
    if event == "P1":
        if value["P1"] == "Player":
            window["P1 name"](visible=True)
            window["P1 level"](visible=False)
        else:
            window["P1 name"](visible=False)
            window["P1 level"](visible=True)

    if event == "P2":
        if value["P2"] == "Player":
            window["P2 name"](visible=True)
            window["P2 level"](visible=False)
        else:
            window["P2 name"](visible=False)
            window["P2 level"](visible=True)

    if value["P1"] != "" and value["P2"] != "":
        window["Play"](disabled=False)

    # if event == "Play":

window.close()
