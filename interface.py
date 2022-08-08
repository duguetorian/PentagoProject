import PySimpleGUI as sg


board, player = {}, 0

layout = [[sg.Text('Board')]]

for row in range(6):
    new_row = []
    for column in range(6):
        new_row.append(sg.Button(size=(2, 1), key=(row, column)))
    layout.append(new_row)

# Create the window
window = sg.Window("Pentago", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

    elif event not in board:
        board[event] = player
        window[event].update(color='white' if player else 'black')

window.close()