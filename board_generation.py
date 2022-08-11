import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def matrix_conversion(matrix):
    table = np.zeros(36).reshape(6, 6)
    for row in range(6):
        for col in range(6):
            if row < 3:
                if col < 3:
                    table[row][col] = matrix[0][0][row][col]
                else:
                    table[row][col] = matrix[1][0][row][col - 3]
            else:
                if col < 3:
                    table[row][col] = matrix[0][1][row - 3][col]
                else:
                    table[row][col] = matrix[1][1][row - 3][col - 3]
    return table


def conversion_to_coordinates(matrix):
    table = matrix_conversion(matrix)
    X0 = []
    X1 = []
    X2 = []
    Y0 = []
    Y1 = []
    Y2 = []
    for row in range(6):
        for col in range(6):
            if table[row][col] == 0.0:
                X0.append(col)
                Y0.append(row)
            if table[row][col] == 1.0:
                X1.append(col)
                Y1.append(row)
            if table[row][col] == 2.0:
                X2.append(col)
                Y2.append(row)
    return (X0, Y0, X1, Y1, X2, Y2)


def generate_figure(matrix):
    X0, Y0, X1, Y1, X2, Y2 = conversion_to_coordinates(matrix)
    fig = plt.figure(figsize=(6, 6))
    fig.set_size_inches(3, 3)
    fig.set_facecolor("darkred")

    ax = fig.add_subplot(111)
    ax.scatter(X0, Y0, s=60, color="dimgrey", marker="o")
    ax.scatter(X1, Y1, s=60, color="white", marker="o")
    ax.scatter(X2, Y2, s=80, color="black", marker="o")
    ax.invert_yaxis()
    ax.set_axis_off()
    ax.vlines(2.5, 0, 5, colors="black")
    ax.hlines(2.5, 0, 5, colors="black")
    
    return fig
