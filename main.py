import PySimpleGUI as sg
from game_interface import game_interface

sg.theme("black")

player_type = ["Player", "AI"]

AI_level = ["Easy", "Hard"]

layout = [
    [sg.Text("Set up the game: ")],
    [
        sg.Text("Player 1"),
        sg.Combo(player_type, key="P1", readonly=True, enable_events=True),
        sg.Input(key="P1 name", default_text=None, visible=False),
        sg.Combo(AI_level, default_value="Easy", key="P1 level", visible=False),
    ],
    [
        sg.Text("Player 2"),
        sg.Combo(player_type, key="P2", readonly=True, enable_events=True),
        sg.Input(key="P2 name", default_text=None, visible=False),
        sg.Combo(AI_level, default_value="Easy", key="P2 level", visible=False),
    ],
    [
        sg.Column(
            [
                [
                    sg.Text("Number of game played"),
                    sg.Input(default_text="10", key="NbGames"),
                ]
            ],
            key="AIvAI",
            visible=False,
        )
    ],
    [
        sg.Column(
            [[sg.Button("Quit"), sg.Button("Play", disabled=True)]],
            justification="right",
        )
    ],
]

window = sg.Window("Pentago Launcher", layout)

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
        if value["P1"] == "AI" and value["P2"] == "AI":
            window["AIvAI"](visible=True)
        else:
            window["AIvAI"](visible=False)

    if event == "P2":
        if value["P2"] == "Player":
            window["P2 name"](visible=True)
            window["P2 level"](visible=False)
        else:
            window["P2 name"](visible=False)
            window["P2 level"](visible=True)
        if value["P1"] == "AI" and value["P2"] == "AI":
            window["AIvAI"](visible=True)
        else:
            window["AIvAI"](visible=False)

    if value["P1"] != "" and value["P2"] != "":
        window["Play"](disabled=False)

    if event == "Play":
        if value["P1"] == "Player":
            p1 = {
                "player1_type": value["P1"],
                "player1_name": value["P1 name"]
                if value["P1 name"] != ""
                else "Player 1",
            }
        else:
            p1 = {
                "player1_type": value["P1"],
                "player1_lvl": value["P1 level"],
            }

        if value["P2"] == "Player":
            p2 = {
                "player2_type": value["P2"],
                "player2_name": value["P2 name"]
                if value["P2 name"] != ""
                else "Player 2",
            }
        else:
            p2 = {
                "player2_type": value["P2"],
                "player2_lvl": value["P2 level"],
            }

        game_interface(
            **p1,
            **p2,
            nb_games=value["NbGames"],
        )

window.close()
