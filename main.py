import numpy as np
from IPython.display import clear_output
import time
import matplotlib.pyplot as plt
from tqdm import tqdm

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
        self.table = np.zeros(36).reshape(2,2,3,3)
        self.winner = None
        self.plot_grid = plot_grid
        
    def play(self, player, position, flip, sens):
        """
        position représente la position de la bille placée,
        flip la position du tableau à pivoter
        dir le sens dans lequel on pivote
        """
        pos = (position[1]//3, position[0]//3, position[0]%3, position[1]%3)
        if self.table[pos] == 0.:
            self.table[pos] = player.number
        else:
            raise ValueError(f'Wrong position : coordinate {position, pos} has value {self.table[pos]}')
        
        self.table[flip] = turn(self.table[flip], sens)
        self.check_winner()
        
    def check_winner(self):
        table = np.concatenate((np.concatenate((game.table[0,0], game.table[0,1])), 
                                np.concatenate((game.table[1,0], game.table[1,1]))), axis=1)
        
        if self.plot_grid:
            clear_output()
            print(table)
        
        winners = []
        
        if 0 not in table:
            if self.plot_grid:
                print('No winners')
            self.winner = 'both'
        
        if not self.winner:
            for i in range(6):
                for j in range(2):
                    if list(table[i,j:j+5]) == [1 for i in range(5)]:
                        winners.append(1)
                    elif list(table[i,j:j+5]) == [2 for i in range(5)]:
                        winners.append(2)

            for j in range(6):
                for i in range(2):
                    if list(table[i:i+5,j]) == [1 for i in range(5)]:
                        winners.append(1)
                    elif list(table[i:i+5,j]) == [2 for i in range(5)]:
                        winners.append(2)
            for j in range(2):
                for i in range(2):            
                    if [table[k+i,k+j] for k in range(5)] == [1 for i in range(5)]:
                        winners.append(1)
                    elif [table[k+i,k+j] for k in range(5)] == [2 for i in range(5)]:
                        winners.append(2)
            
            
            if 1 in winners and 2 not in winners:
                if self.plot_grid:
                    print('Player 1 wins')
                self.winner = 1
                
            elif 1 not in winners and 2 in winners:
                if self.plot_grid:
                    print('Player 2 wins')
                self.winner = 2

            elif 1 in winners and 1 not in winners:
                if self.plot_grid:
                    print('No winners')
                self.winner = 'both'
        
class player:
    
    def __init__(self, number):
        if number == 1 or number == 2:
            self.number = number
        else:
            raise ValueError('Invalid number')
                        
    def play(self, position, flip, sens, game):
        game.play(self, position, flip, sens)
        
    def random_play(self, game):
        """
        plays a random case, flips a random case in a random direction
        """
        state = True
        while state:
            position = np.random.randint(0,6,size=2)
            pos = (position[1]//3, position[0]//3, position[0]%3, position[1]%3)
            flip = tuple(np.random.randint(0,2,size=2))
            sens = [1, -1][int(np.random.randint(0,2,size=1))]
            if game.table[pos] == 0:
                self.play(position, flip, sens, game)
                state = False
                
    def smart_play(self, game):
        """
        trouve la plus longue chaine de pièces et la complète,
        tourne la table de façon à ne pas détruire sa chaine la plus longue
        """
        
        table = np.concatenate((np.concatenate((game.table[0,0], game.table[0,1])), 
                                np.concatenate((game.table[1,0], game.table[1,1]))), axis=1)
        
        pieces_coor = [(np.where(table == self.number)[0][i], np.where(table == self.number)[1][i]) for i in range(np.size(np.where(table == self.number))//2)] 
        zeros_coor = [(np.where(table == 0)[0][i], np.where(table == 0)[1][i]) for i in range(np.size(np.where(table == 0))//2)] 

        
        max_length = 0
        max_length_coor = None
        flip = (0, 0)
        
        for x in pieces_coor:
            
            #vertical chains
            length = 0
            while (x[0], x[1]+length) in pieces_coor:
                length += 1
                
            if length > max_length:
                
                if x[1]+length <= 5:
                    max_length_coor = (x[0], x[1]+length)
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                else:
                    max_length_coor = (x[0], x[1]-1)
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                if max_length_coor:
                    max_length = length
                    flip = ([0,1][max_length_coor[0]//3 - 1], 
                            max_length_coor[1]//3)
                
            #horizontal chains    
            length = 0
            while (x[0]+length, x[1]) in pieces_coor:
                length += 1
                
            if length > max_length:
                
                if x[0]+length <= 5:
                    max_length_coor = (x[0]+length, x[1])
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                else:
                    max_length_coor = (x[0]-1, x[1])
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                if max_length_coor:
                    max_length = length
                    flip = (max_length_coor[0]//3, 
                            [0,1][max_length_coor[1]//3 - 1])

            #diagonal chains    
            length = 0
            while (x[0]+length, x[1]+length) in pieces_coor:
                length += 1
                
            if length > max_length:
                
                if x[0]+length <= 5 and x[1]+length <= 5:
                    max_length_coor = (x[0]+length, x[1]+length)
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                elif x[0]+length <= 5 and x[1]+length > 5:
                    max_length_coor = (x[0]+length, x[1]-1)
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                elif x[0]+length > 5 and x[1]+length <= 5:
                    max_length_coor = (x[0]-1, x[1]+length)
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                else:
                    max_length_coor = (x[0]-1, x[1]-1)
                    if max_length_coor not in zeros_coor:
                        max_length_coor = None
                if max_length_coor:
                    max_length = length
                    flip = ([0,1][max_length_coor[0]//3 - 1], 
                            [0,1][max_length_coor[1]//3 - 1])
        if max_length_coor:
            
            self.play(max_length_coor, flip, 1, game)
        
        else:
            
            self.random_play(game) #plays randomly if there are no chains

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