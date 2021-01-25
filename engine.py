import copy

class Move:
    def __init__(self, coord=0, hacked=[], contineous=True):
        self.coord = coord
        self.hacked = hacked
        self.contineous = contineous
        self.next_move = 0
        self.out_vector = 0

    def correct_coord(self, dict_correct):
        if self.coord in dict_correct.keys():
            self.coord = dict_correct[self.coord]
        #print(self.hacked)
        new_hacked = []
        for hack in self.hacked:
            if hack in dict_correct.keys():
                new_hacked.append(dict_correct[hack])
            else:
                raise 'Bad hack'
        self.hacked = new_hacked

    def __eq__(self, other):
        # сравнение двух прямоугольников
        if isinstance(other, Move):
            return self.coord == other.coord
        # иначе возвращаем NotImplemented
        return NotImplemented

    def transform(self, dict_correct):
        if self.coord in dict_correct.keys():
            coord = dict_correct[self.coord]
        print(coord)

    def __repr__(self):
        return 'Move' + str(self.coord)  #+ ' hack=' + str(self.hacked) + ' cont=' + str(self.contineous) + '    ' + str(self.next_move)

class VectorMove:
    def __init__(self):
        self.moves = {}
    
    def add_move(self, vector:tuple, move:Move):
        if vector in self.moves.keys():
            self.moves[vector].append(move)
        else:
            self.moves[vector] = [move]
    
    def get_all_vectors(self):
        return list(self.moves.keys())

    def get_all_vector_moves(self, vector:tuple):
        if vector in self.moves.keys():
            return self.moves[vector]
        return 0
    
    def remove_in_vector(self, vector:tuple, move:Move):
        if vector in self.moves.keys():
            self.moves[vector].remove(move)

class Figure:
    def __init__(self, color='u', pos = (-1,-1), area=[]):
        self.name = 'F'        
        self.color = color        
        self.color_enemy = 'w' if color[0] == 'b' or color[0] == 'd' else 'b'
        #print((self.color, self.color_enemy))
        self.name = 'P' if color == 'w' or color == 'b' else 'Q'
        self.pos = pos
        self.area = area
        self.next_moves = []
        self.is_hack = False
        self.is_clone = False
        
        self.direction = 1 if color == 'b' else -1
    
    def check_borders(self, p):
        if p >= 0 and p < 8:
            return True
        return False
    
    def check_figure(self, x, y, color=0):
        if self.check_borders(y) and self.check_borders(x):
            return self.area[y][x]
        else:
            return 'x'

    def make_move_get_hacking(self, figure, r_area, move):
        area = copy.deepcopy(r_area) 
        f = copy.deepcopy(figure)
        # Запоминаем фигуру
        chess = area[f.pos[1]][f.pos[0]]
        # Поднимаем фигуру
        area[f.pos[1]][f.pos[0]] = '.'
        # Делам ход
        area[move.coord[1]][move.coord[0]] = chess
        # Убираем срубленное
        area[move.hacked[-1][1]][move.hacked[-1][0]] = '.'
        area = self.check_queens(area)
        f.pos = move.coord
        f.area = area
        return f.have_hacking(0,0,move.out_vector)

    def get_queen_color(self, color='u'):
        if color[0] == 'w':            
            return 'D'
        if color[0] == 'b':            
            return 'd'
        return 'x'

    def check_queens(self, area=0):
        main_area = area if area else self.area       
        j = 0            
        for i in range(0,8):
            if main_area[j][i] == 'w':
                main_area[j][i] = 'D'
        j = 7            
        for i in range(0,8):
            if main_area[j][i] == 'b':
                main_area[j][i] = 'd'
        return main_area

    def __repr__(self):
        return self.name + '[' + self.color + ']=' + str(self.pos)


class Pawn(Figure):
    '''
    Сhecker as English
    '''   
    def get_not_hacking_poses(self):
        y = self.pos[1] + self.direction  
        # Стандартный ход вперёд
        for x in range( self.pos[0] - 1, self.pos[0] + 2, 2):
            if self.check_borders(y) and self.check_borders(x):
                if self.check_figure(x,y) == '.':
                    self.next_moves.append(Move((x,y), [], False))
        return self.next_moves

    def have_hacking(self, figure=0, area=0, out_vector=0):
        main_area = area if area else self.area            
        pos = figure.pos if figure else self.pos

        for i in range(2):
            mark_y = 1 if (i + 1) % 2 == 0  else -1 
            y = pos[1] + 2 * mark_y
            for mark_x in range(-1, 2, 2):
                if out_vector and mark_x == out_vector[0] and mark_y == out_vector[1] :
                    continue
                x = pos[0] + 2 * mark_x
                if self.check_borders(y) and self.check_borders(x):
                    if self.check_figure(x, y) == '.':
                        f_str = self.check_figure(x - mark_x, y - mark_y)    
                        if f_str == self.color_enemy or f_str == self.get_queen_color(self.color_enemy):                                        
                            return True
        return False

    def get_hacking_poses(self, figure=0, area=0, out_vector=0):
        next_moves = []
        main_area = area if area else self.area           
        pos = figure.pos if figure else self.pos
        
        for i in range(2):
            mark_y = 1 if (i + 1) % 2 == 0  else -1 
            y = pos[1] + 2 * mark_y
            for mark_x in range(-1, 2, 2):
                if out_vector and mark_x == out_vector[0] and mark_y == out_vector[1] :
                    continue

                x = pos[0] + 2 * mark_x
                if self.check_borders(y) and self.check_borders(x):
                    if self.check_figure(x, y) == '.':                                                                  
                        f_str = self.check_figure(x - mark_x, y - mark_y)                        
                        if f_str == self.color_enemy or f_str == self.get_queen_color(self.color_enemy):
                            if out_vector == 0:
                                move = Move((x, y), [(x - mark_x, y - mark_y)])
                                move.contineous = self.make_move_get_hacking(self, self.area, move)
                                self.next_moves.append(move)                            
                            else:      
                                next_moves.append( Move((x, y), [(x - mark_x, y - mark_y)]))                   
                            self.is_hack = True
        if out_vector == 0:
            return self.next_moves
        return next_moves

    def get_next_hack_moves(self):        
        # Рубим
        c = Computer(copy.deepcopy(self.area), self.pos, self.color)
        print(self.color)
        print('res = ' + str(c.calc_all_hacking3(self, self.area)))
        
        #self.next_moves, f = c.calc_all_hacking2(self)
 
        return self.next_moves


class Queen(Figure):
    '''
    King as English
    '''
    def get_not_hacking_poses(self):
        if self.is_clone:
            return self.pos
        for j in range(4):            
            mark_x = -1 if (j+1) % 2 == 0 else 1
            mark_y = 1 if j < 2 else -1 
            #print((mark_x, mark_y))
            for i in range(1,8):
                y = self.pos[1] + i * mark_y           
                x = self.pos[0] + i * mark_x
                #print(x,y)
                if self.check_borders(y) and self.check_borders(x):
                    #print(x,y)
                    if self.check_figure(x,y) == '.':
                        #self.next_moves[(x,y)] = [[(x-1,y-self.direction * mark_y)], False]
                        self.next_moves.append(Move((x,y), [], False))
                    else:
                        break
                else:
                    break
        return self.next_moves

    def have_hacking(self, figure=0, area=0, out_vector=0):
        main_area = area if area else self.area        
        pos = figure.pos if figure else self.pos

        for j in range(4):            
            mark_x = -1 if (j+1) % 2 == 0 else 1
            mark_y = 1 if j < 2 else -1 
            if out_vector and mark_x == out_vector[0] and mark_y == out_vector[1] :
                    continue

            #print((mark_x, mark_y))
            for i in range(1,8):
                y = pos[1] + i * mark_y           
                x = pos[0] + i * mark_x


                if self.check_borders(y) and self.check_borders(x):
                    f_str = self.check_figure(x,y)    
                    if f_str == self.color_enemy or f_str == self.get_queen_color(self.color_enemy): 
                    #if self.check_figure(x,y) == self.color_enemy:
                        if self.check_figure(x + mark_x, y + mark_y) == '.': 
                            return True                   
                        else:
                            break
                else:
                    break
        return False
    
    def get_hacking_poses(self, figure=0, area=0, out_vector=0):
        next_moves = []
        main_area = area if area else self.area           
        pos = figure.pos if figure else self.pos
                
        # Рубим
        for j in range(4):            
            mark_x = -1 if (j+1) % 2 == 0 else 1
            mark_y = 1 if j < 2 else -1 
            if out_vector and mark_x == out_vector[0] and mark_y == out_vector[1] :
                continue
            #print((mark_x, mark_y))
            for i in range(1,8):
                y = self.pos[1] + i * mark_y           
                x = self.pos[0] + i * mark_x

                if self.check_borders(y) and self.check_borders(x):
                    f_str = self.check_figure(x,y)    
                    if f_str == self.color_enemy or f_str == self.get_queen_color(self.color_enemy):                        
                        moves = []
                        cont = False
                        for k in range(1,8):
                            if self.check_figure(x + mark_x * k, y + mark_y * k) == '.':
                                move = Move((x + mark_x * k, y + mark_y * k), [(x, y)])
                                move.out_vector = (mark_x * -1, mark_y * -1)
                                move.contineous = self.make_move_get_hacking(self, self.area, move)
                                cont = cont or move.contineous
                                moves.append(move)
                                self.is_hack = True
                            else:
                                break
                        print('moves = ' + str(moves))
                        print('cont = ' + str(cont))
                        if cont:
                            self.next_moves = [move for move in moves if move.contineous == cont]
                        else:
                            self.next_moves = self.next_moves + moves
                        print('self.next_moves = ' + str(self.next_moves))
                        
                        # for k in range(1,8):
                        #     if self.check_figure(x + mark_x * k, y + mark_y * k) == '.':
                        #         #if out_vector == 0:
                        #         move = Move((x + mark_x * k, y + mark_y * k), [(x, y)])
                        #         move.out_vector = (mark_x * -1, mark_y * -1)
                        #         move.contineous = self.make_move_get_hacking(self, self.area, move)

                        #         self.next_moves.append()                         
                        #         #else:
                        #         #    next_moves.append(Move((x + mark_x * k, y + mark_y * k), [(x, y)], False))
                                
                        #         self.is_hack = True
                        #     else:
                        #         break
                        break
                else:
                    break
        #if out_vector == 0:
        return self.next_moves
        #else:               
        #    return next_moves

    def get_next_hack_moves(self):        
        # Рубим
        c = Computer(copy.deepcopy(self.area), self.pos, self.color)
        print(self.color)
        print('res = ' + str(c.calc_all_hacking3(self, self.area)))

class Board:
    def __init__(self):
        # Буквы и цифры на доске
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
        
        self.figures = []
        self.moving_figures = []
        self.hacking_figures = []
        self.dict_moves = {}
    

        # Создадим доску 8x8
        '''
        self.area[0][0] = 'F'
        self.area[0][1] = '→' # '/u2192'
        self.area[1][0] = '↓' # '/u2193'
        self.area[7][7] = 'E'

        print(self)

        8| F → . . . . . .
        7| ↓ . . . . . . .
        6| . . . . . . . .
        5| . . . . . . . .
        4| . . . . . . . .
        3| . . . . . . . .
        2| . . . . . . . .
        1| . . . . . . . E
        ------------------
           A B C D E F G H
        '''
        self.area = []
        for j in range(0,8):
            self.area.append([])
            for i in range(0,8):
                self.area[j].append('.')

    def set_figures(self, positions):
        for j in range(0,8):            
            for i in range(0,8):
                self.area[j][i] = '.'
        if type(positions) == type([]):
            for pos, color in positions:
                self.area[pos[1]][pos[0]] = color[0]
        print(self)

    def exchange_figures(self, color='u'):
        self.figures = []
        self.moving_figures = []
        print('color b = ' + color) 
        if color == 'd':
            color = 'b'
        if color == 'D':
            color = 'w'
        print('color a = ' + color) 
        for j in range(0,8):            
            for i in range(0,8):                
                if self.area[j][i] != '.':
                    damka = 'd' if color[0] == 'b' else 'D'
                    if self.area[j][i] != color[0] and damka != self.area[j][i]:
                        print((self.area[j][i], color[0], damka))
                        if self.area[j][i].lower() == 'd':
                            self.moving_figures.append(Queen(self.area[j][i], (i,j), self.area))
                        else:
                            self.moving_figures.append(Pawn(self.area[j][i], (i,j), self.area))
                if self.area[j][i] != '.':
                    if self.area[j][i].lower() == 'd':
                        self.figures.append(Queen(self.area[j][i], (i,j), self.area))
                    else:
                        self.figures.append(Pawn(self.area[j][i], (i,j), self.area))
        print('self.moving_figures') 
        print(self.moving_figures) 
        
        self.hacking_figures = []
        for f in self.moving_figures:
            if f.have_hacking():
                self.hacking_figures.append(f)
        
        dict_moves = {}
        if len(self.hacking_figures):
            # Есть что срубить
            for f in self.hacking_figures:
                dict_moves[f.pos] = f.get_hacking_poses()
                #print(f.get_hacking_poses())
             
        else:
            # Обычный ход
            for f in self.moving_figures:
                dict_moves[f.pos] = f.get_not_hacking_poses()

        self.dict_moves = dict_moves
        print(self.dict_moves)
        return dict_moves

    # Распечатка доски
    def __repr__(self):
        s = ''
        for j in range(0,8):#(7,-1,-1):
            s += str(self.numbers[7-j]) + '| ' 
            for i in range(0,8):
                s += self.area[j][i] + ' '
            s += '\n'
        
        for i in range(0,18):
            s += '-'
        s += '\n   '
        for i in range(0,8):
            s += self.letters[i] + ' '
        s += '\n'
        return s

class Computer:
    def __init__(self, area, pos=0, color_move='u'):
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
        
        self.area = area
        self.hacking = {}
        #self.hacking_all = []
        self.pos = pos
        self.all_moves = []
        self.color_move = color_move
        self.get_info()
    

    def check_queens(self, area=0):
        main_area = area if area else self.area       
        j = 0            
        for i in range(0,8):
            if main_area[j][i] == 'w':
                main_area[j][i] = 'D'
        j = 7            
        for i in range(0,8):
            if main_area[j][i] == 'b':
                main_area[j][i] = 'd'
        return main_area

    def make_move(self, figure, area, move):
        area = copy.deepcopy(area) 
        f = copy.deepcopy(figure)
        # Запоминаем фигуру
        chess = area[f.pos[1]][f.pos[0]]
        # Поднимаем фигуру
        area[f.pos[1]][f.pos[0]] = '.'
        # Делам ход
        area[move.coord[1]][move.coord[0]] = chess
        # Убираем срубленное
        area[move.hacked[-1][1]][move.hacked[-1][0]] = '.'
        area = self.check_queens(area)
        f.pos = move.coord
        f.area = area
        return f, area

    def calc_all_hacking3(self, figure, area=0):  
        main_area = area if area else self.area      
        dict_moves[figure.pos] = []
        for vector in figure.next_moves.get_all_vectors():
            hacking_figures = []
            for move in figure.next_moves.get_all_vector_moves(vector):
                new_fig, new_area = self.make_move(figure, main_area, move)                
                if new_fig.have_hacking(new_fig, new_area, vector):
                    self.hacking_figures.append(new_fig)
            if len(hacking_figures):
                pass
            else:
                dict_moves[figure.pos].append()



            #print(self.calc_all_hacking2(f, area))



        return f.next_moves
 

    def get_info(self, area=0):
        self.figures = []
        self.moving_figures = []
        self.exchange_figures(self.color_move, area=0)

    def get_figure_by_pos(self, pos):
        for f in self.figures:
            if f.pos == pos:
                return f
        return 0

    def exchange_figures(self, color='u', area=0):
        self.figures = []
        self.moving_figures = []
        if area:
            main_area = area            
        else:
            main_area = self.area
        for j in range(0,8):            
            for i in range(0,8):
                if main_area[j][i] != color[0] and main_area[j][i] != '.':
                    if main_area[j][i].lower() == 'd':
                        self.moving_figures.append(Queen(main_area[j][i], (i,j), main_area))
                    else:
                        self.moving_figures.append(Pawn(main_area[j][i], (i,j), main_area))
                if main_area[j][i] != '.':
                    if main_area[j][i].lower() == 'd':
                        self.figures.append(Queen(main_area[j][i], (i,j), main_area))
                    else:
                        self.figures.append(Pawn(main_area[j][i], (i,j), main_area))

    # Распечатка доски
    def print_area(self, area):
        s = '#########COMPUTER#########\n'
        for j in range(0,8):#(7,-1,-1):
            s += str(self.numbers[7-j]) + '| ' 
            for i in range(0,8):
                s += area[j][i] + ' '
            s += '\n'
        
        for i in range(0,18):
            s += '-'
        s += '\n   '
        for i in range(0,8):
            s += self.letters[i] + ' '
        s += '\n'
        return s

    # Распечатка доски
    def __repr__(self):
        s = '#########COMPUTER#########\n'
        for j in range(0,8):#(7,-1,-1):
            s += str(self.numbers[7-j]) + '| ' 
            for i in range(0,8):
                s += self.area[j][i] + ' '
            s += '\n'
        
        for i in range(0,18):
            s += '-'
        s += '\n   '
        for i in range(0,8):
            s += self.letters[i] + ' '
        s += '\n'
        return s

if __name__ == "__main__":
    b = Board()
    #b.set_figures( [ [(0,7), 'w'], [(3,6), 'b'], [(1,6), 'b'], [(5,6), 'b'] ] )
    #b.set_figures( [ [(2,7), 'w'], [(3,6), 'b'], [(1,6), 'b'], [(2,2), 'w'],  [(3,1), 'b'], [(1,1), 'b'] ] )

    b.set_figures( [ [(0,7), 'D'], [(1,6), 'b']] )
    #b.set_figures( [ [(0,7), 'D'], [(1,6), 'b'], [(3,4), 'b'] ] )
    #b.set_figures( [ [(0,7), 'D'], [(4,6), 'b'] ] )

    #b.set_figures( [ [(1,6), 'w'], [(1,4), 'b'] ] )
    b.exchange_figures('b')
    print(b)