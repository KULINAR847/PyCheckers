import sys
import copy

from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

from engine import Board, Move

class StaticItem(QGraphicsPixmapItem):
    def __init__(self, path='', pos=0, enable=False, parent=None):
        super().__init__(parent)
        self.path = path
        #self.alive = alive
        self.side = 70
        self.pixmap = QPixmap(self.path).scaled(self.side, self.side)
        self.setPixmap(self.pixmap)
        if type(pos) == type(()):
            self.setPos(pos[0], pos[1])
        elif pos:
            self.setPos(pos.x(), pos.y())

class MoveItem(QGraphicsPixmapItem):
    #changed_pos = Signal(str)    

    def __init__(self, path='', alive=False, enable=False, parent=None):
        super().__init__(parent)
        self.available_coords = []
        self.work_coords = []
        self.transform_dict = {}
        self.path = path
        self.alive = alive
        self.enable = enable
        self.color = 'b' if 'black' in path else 'w'
        self.color_enemy = 'w' if self.color[0] == 'b' or self.color[0] == 'd' else 'b'
        self.side = 70
        self.old_position = (-1,-1)      
        self.signalizer = Signalizer()
        self.pixmap = QPixmap(self.path).scaled(self.side, self.side)
        self.w = self.pixmap.width()
        self.h = self.pixmap.height()
        self.half_width = int(self.pixmap.width()/2)
        self.half_height = int(self.pixmap.height()/2)
        self.setPixmap(self.pixmap)
        self.next_positions = []
        self.hacked = []
        self.contineous = False
        self.border_y = 0
        #self.board = 0
        self.next_moves = []

    def __repr__(self):
        return 'MoveItem [' + str(self.color) + ' | ' + str(self.color_enemy) + ' ' + str( self.pos() ) + ']'

    def boundingRect(self):
        return self.pixmap.rect()

    def paint(self, painter, option, widget):
        painter.drawPixmap(self.pixmap.rect(), self.pixmap)

    def set_next_positions(self, next_positions=[]):
        if len(next_positions) == 0:
            self.enable = False
        else:
            self.next_positions = next_positions

    def mouseMoveEvent(self, event): 
        if self.alive and self.enable:      
            new_pos = copy.deepcopy(event.pos())
            #print(self.pos())
            new_pos.setX(new_pos.x() - self.half_width)
            new_pos.setY(new_pos.y() - self.half_height)
            self.setPos(self.mapToScene(new_pos))
    
    def mousePressEvent(self, event):
        if self.alive and self.enable:
            self.setCursor(QCursor(Qt.ClosedHandCursor))               
            if type(self.work_coords) == type([]):
                min_len = 1000000
                min_coord = 0
                for move in self.work_coords:
                #work_coords = [move.coord for move in self.work_coords]
                #for coord in work_coords:
                    #print(move)
                    length = (move.coord[0] - self.pos().x()) ** 2 + (move.coord[1] - self.pos().y()) ** 2
                    #print(self.pos())
                    #print(move, length)
                    if length < min_len:
                        #print(min_len)
                        min_len = length
                        min_coord = move
                if min_coord:
                    #print(self.transform_dict)
                    #print(move.transform(self.transform_dict))
                    self.old_position = min_coord
                    self.available_coords.append(min_coord)
                    #print(self.available_coords)
                    #print(self.next_positions)
                    #self.next_moves = self.board.dict_moves[min_coord]

    
    def mouseReleaseEvent(self, event):
        if self.alive and self.enable:
            self.setCursor(QCursor(Qt.ArrowCursor))
            if type(self.available_coords) == type([]):
                min_len = 1000000
                min_coord = 0
                #available_coords = [move.coord for move in self.available_coords]
                for move in self.available_coords:
                    length = (move.coord[0] - self.pos().x()) ** 2 + (move.coord[1] - self.pos().y()) ** 2
                    if length < min_len :
                        min_len = length
                        min_coord = move
                # for coord in available_coords:
                #     length = (coord[0] - self.pos().x()) ** 2 + (coord[1] - self.pos().y()) ** 2
                #     if length < min_len:
                #         min_len = length
                #         min_coord = coord
                print(min_coord)
                #print(self.next_positions)
                #print(min_coord)
                #print(self.available_coords)
                # next_positions = [move.coord for move in self.next_positions]
                # if min_coord in next_positions:
                #     move = [move.coord for move in self.next_positions if move.coord == min_coord][0]
                    
                #     self.setPos(min_coord[0], min_coord[1])
                #     if type(move) == type(Move()) and move.hacked:
                #         self.hacked.append(move.hacked)
                    #self.contineous = self.next_positions[min_coord][1]
                    # if self.contineous:
                    #     keys = []                            
                    #     for k, v in self.next_positions.items():
                    #         print('v = ' + str(v))
                    #         if len(v[0]) < len(self.hacked):
                    #             keys.append(k)
                    #     for key in keys:
                    #         self.available_coords.pop(key, None)
                    #         self.next_positions.pop(key, None)
                #available_coords = [move.coord for move in self.available_coords]
                if min_coord in self.available_coords:

                    if min_coord != self.old_position: 
                        print('self.next_moves = ' + str(self.next_positions))
                        if min_coord in self.next_positions:
                            move = self.next_positions[self.next_positions.index(min_coord)]
                            self.hacked = move.hacked
                            self.contineous = move.contineous

                        # for move in self.next_positions:
                        #     #print('GOOOOOOOOOOOOOOOOOOOD')
                        #     if move.coord == min_coord.coord:
                        #         self.hacked = move.hacked                     
                        # self.signalizer.changed_pos.emit(self)
                              
                            self.available_coords.remove(min_coord)                    
                            self.setPos(min_coord.coord[0], min_coord.coord[1])
                            #self.available_coords.append(self.old_position)
                            #print(self.available_coords)
                            if min_coord.coord[1] == self.border_y:
                                self.make_queen()

                            self.signalizer.changed_pos.emit(self)
                        else:
                            self.available_coords.remove(self.old_position)
                            self.setPos(self.old_position.coord[0], self.old_position.coord[1])
                    else:
                        self.available_coords.remove(self.old_position)
                        self.setPos(self.old_position.coord[0], self.old_position.coord[1])

                else:
                    self.available_coords.remove(self.old_position)
                    self.setPos(self.old_position.coord[0], self.old_position.coord[1])

                #print(self.available_coords)
                #if min_coord in self.next_positions:
                #    self.signalizer.changed_pos.emit(self)
                
    def make_queen(self):
        if self.color[0] == 'b':
            self.path = 'black_queen.png'
            self.pixmap = QPixmap(self.path).scaled(self.side, self.side)
            self.color = 'd'
        if self.color[0] == 'w':
            self.path = 'white_queen.png'
            self.pixmap = QPixmap(self.path).scaled(self.side, self.side)
            self.color = 'D'
    
    def make_pawn(self):
        if self.color == 'd':
            self.path = 'black.png'
            self.pixmap = QPixmap(self.path).scaled(self.side, self.side)
            self.color = 'b'
        if self.color == 'D':
            self.path = 'white.png'
            self.pixmap = QPixmap(self.path).scaled(self.side, self.side)
            self.color = 'w'

        #self.changed_pos.emit("Hello everybody!")

class Signalizer(QObject):
    changed_pos = Signal(MoveItem)    

class Shashki(QWidget):
    def __init__(self, parent=None): 
        super().__init__(parent)

        self.setWindowTitle('Шашки') 

        layout = QGridLayout(self)
        self.setLayout(layout)
        
        self.left = 117
        self.top = 120

        # Режим игры
        # 0 - нерасставленные фигуры
        # 1 - ручная растановка
        # 2 - автоматическая расстановка
        # 3 - игра
        # 4 - продолжение хода
        self.mode = 1 

        self.board = Board() # Движок

        self.static_items = []

        self.coord_straight = {} # { (0,1) : (117,190), ...  }
        self.coord_reverse = {}  # { (117,190) : (0,1), ...  }

        self.scene = QGraphicsScene()
        
        self.view = QGraphicsView()
        layout.addWidget(self.view,0,0)

        def openMenu(position):
			# Создание PopupMenu
            menu = QMenu()
            playStopAction, autoAction, reAutoAction, contWhiteAction, contBlackAction = QAction(), QAction(), QAction(), QAction(), QAction()			
            if self.mode >= 3:				
                playStopAction = menu.addAction('Остановить игру')
            elif self.mode < 3:				
                playStopAction = menu.addAction('Начать игру')
                menu.addSeparator()
                autoAction = menu.addAction('Автоматическая расстановка')
                reAutoAction = menu.addAction('Автоматическая сборка')
                menu.addSeparator()
                contWhiteAction = menu.addAction('Продолжить белыми')
                contBlackAction = menu.addAction('Продолжить чёрными')
                menu.addSeparator()

            quitAction = menu.addAction('Выход')
            action = menu.exec_(self.mapToGlobal(position))
            
            # Привязка событий к Actions					
            if action == playStopAction:
                self.play_stop()	
                
            if action == autoAction:
                self.set_start_pos()

            if action == reAutoAction:
                self.set_null_pos()

            if action == contWhiteAction:
                self.continue_white()	

            if action == contBlackAction:
                self.continue_black()

            if action == quitAction:
                self.accept()

        self.view.setContextMenuPolicy(Qt.CustomContextMenu)		  
        self.view.customContextMenuRequested.connect(openMenu)
 
        self.view.setScene(self.scene)

        self.groups = []
        self.group_b = []
        self.group_w = []
        
        self.scene.addPixmap(QPixmap('back.jpg'))
        self.resize(self.scene.width()+60, self.scene.height()+60)

        for i in range(12):
            item = MoveItem('black.png', True, self.mode != 3)  
            item.setPos(i* item.w, 30)  
            item.board = self.board
            item.signalizer.changed_pos.connect(self.chess_moved)            
            self.scene.addItem(item)
            self.group_b.append(item) 

        for i in range(12):
            item = MoveItem('white.png', True, True)                
            item.setPos(i* item.w, 700)
            item.board = self.board
            item.signalizer.changed_pos.connect(self.chess_moved)                 
            self.scene.addItem(item)
            self.group_w.append(item)  
        
        self.groups = self.group_w + self.group_b
        
        self.work_coords = []
        self.available_coords = []
        for j in range(8):
            for i in range(8):
                if j % 2 == 0: 
                    if i % 2 != 0:    
                        self.coord_straight[(i,j)] =  (i * item.w + self.left, j * item.h + self.top)                 
                        self.work_coords.append(Move((i * item.w + self.left, j * item.h + self.top)))
                else:
                    if i % 2 == 0:    
                        self.coord_straight[(i,j)] =  (i * item.w + self.left, j * item.h + self.top)                                  
                        self.work_coords.append( Move((i * item.w + self.left, j * item.h + self.top)) )
        self.coord_reverse = {v:k for k, v in self.coord_straight.items()}

        self.available_coords = copy.deepcopy(self.work_coords)

        for item in self.groups:
            item.transform_dict = self.coord_reverse

        #print(self.work_coords)

        if len(self.work_coords) == 32:
            min_y = min([10000] + [ move.coord[1] for move in self.work_coords ] )
            max_y = max([0] + [ move.coord[1] for move in self.work_coords ] )
            print('min_y = ' + str(min_y))
            print('max_y = ' + str(max_y))

            for item in self.groups:
                item.available_coords = self.available_coords
                item.work_coords = self.work_coords
                item.next_positions = self.available_coords
                if item.color[0] == 'b':
                    item.border_y = max_y
                else:
                    item.border_y = min_y


    def deactivate_outs(self):
        work_coords = [ move.coord for move in self.work_coords ]
        #print(work_coords)
        for item in self.groups:
            #print((item.pos().x(), item.pos().y()))           

            if (item.pos().x(), item.pos().y()) in work_coords:
                item.alive = True
                item.contineous = False
            else:
                item.alive = False
    
    def activate_all(self):
        for item in self.groups:
            item.alive = True
            item.enable = True
            item.next_positions = self.available_coords
    
    def play_stop(self):
        if self.mode == 3:
            self.mode = 1
            self.activate_all()
        else:
            print('play')
            self.mode = 3
            self.setWindowTitle('Идёт игра!') 
            self.deactivate_outs()
            self.chess_moved(self.group_b[0])	

    def set_start_pos(self):
        upper_coords = self.get_upper_3_lines_coords()        
        self.setWindowTitle('Шашки')
        #print(upper_coords) 
        #print(self.available_coords) 
        if upper_coords:
            if len(self.group_b) == len(upper_coords):
                for i, move in enumerate(upper_coords):
                    #print(id(move))
                    #print([id(move) for move in self.available_coords])
                    #for move in self.available_coords:
                    #if move.coord[0] == 
                    self.available_coords.remove(move)
                    self.group_b[i].setPos(move.coord[0], move.coord[1])
                    #print(self.move)
                    
                    #self.available_coords.remove(p)

        lower_coords = self.get_lower_3_lines_coords()
        #print(lower_coords)
        if lower_coords:
            if len(self.group_w) == len(lower_coords):
                for i, move in enumerate(lower_coords):
                    self.group_w[i].setPos(move.coord[0], move.coord[1])
                    self.available_coords.pop(self.available_coords.index(move))
                    #self.available_coords.remove(p)

        print(self.available_coords)

    def find_move_in_available(self, move):
        pass

    def set_null_pos(self):
        self.setWindowTitle('Шашки') 
        self.available_coords = copy.deepcopy(self.work_coords)
        self.activate_all()
        for i, item in enumerate(self.group_b):            
            item.setPos(i* item.w, 30)             
            item.available_coords = self.available_coords            
            item.next_positions = self.available_coords 
            item.make_pawn()        

        for i, item in enumerate(self.group_w):                      
            item.setPos(i* item.w, 700)            
            item.available_coords = self.available_coords            
            item.next_positions = self.available_coords 
            item.make_pawn()

    def continue_white(self):
        self.mode = 3
        self.setWindowTitle('Идёт игра!') 
        self.deactivate_outs()
        self.chess_moved(self.group_b[0])	

    def continue_black(self):
        self.mode = 3
        self.setWindowTitle('Идёт игра!') 
        self.deactivate_outs()
        self.chess_moved(self.group_w[0])

    def get_upper_3_lines_coords(self):
        if len(self.work_coords) == 32:
            return self.work_coords[:12]
        else:
            print('Bad work_coord length!')
            return 0

    def get_lower_3_lines_coords(self):
        if len(self.work_coords) == 32:
            return self.work_coords[-12:]
        else:
            print('Bad work_coord length!')
            return 0
    
    def get_items_pos(self):
        positions = []
        for item in self.groups:
            if item.alive:
                positions.append([self.coord_reverse[(int(item.pos().x()), int(item.pos().y()))], item.color])
        return positions

    def get_item_by_coord(self, pos):
        for item in self.groups:
            if item.pos().x() == pos[0] and item.pos().y() == pos[1]:
                return item
        return 0

    def show_message(self, title='', text=''):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setFont(QFont('TimesNewRoman', 15))
        result = msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def get_out_item(self, item):
        if item.color[0] == 'b':
            y = 30
            x = (len(self.group_b) - sum([1 for item in self.group_b if item.alive])) * item.w 
        else:
            y = 700
            x = (len(self.group_w) - sum([1 for item in self.group_w if item.alive])) * item.w
        print('del out = ' + str( (x,y) ) )
        item.alive = False
        self.available_coords.append(Move( (int(item.pos().x()), int(item.pos().y()))   ))
        item.setPos(x, y)

    def chess_moved(self, ritem):
        #pass
        #         item.enable = ritem.color != item.color
        print('\nNEW MOVE in mode = ' + str(self.mode))
        if self.mode == 3:
            delfigs = ritem.hacked
            print('delfigs = ' + str(delfigs))
            if len(delfigs) > 0:
                for move in delfigs:
                    print('del figure')
                    item = self.get_item_by_coord( move )
                    if item:
                        self.get_out_item(item)
                        #item.setPos(0, 0)
                        #item.alive = False

            if ritem.contineous:
                #self.mode = 4
                for item in self.groups:
                    item.enable = ritem == item 
            else:
                for item in self.groups:                    
                    item.enable = ritem.color_enemy != item.color_enemy
                    if item.alive:
                        print((item, item.enable and item.alive, item.color_enemy, ritem.color_enemy))      
            
            self.board.set_figures(self.get_items_pos())
            if ritem.contineous:
                self.board.exchange_figures(ritem.color_enemy)
            else:
                self.board.exchange_figures(ritem.color)   

            moves = []
            for stat_item in self.static_items:
                self.scene.removeItem(stat_item)
            self.static_items.clear()

            print(self.board.moving_figures)
            for f in self.board.moving_figures:
                next_positions = []
                #print(f.next_moves)
                for move in f.next_moves:
                    #print(move)
                    moves.append(move)
                    move.correct_coord(self.coord_straight)
                    #move.transform(self.coord_reverse)
                    stat_item = StaticItem('fig.png', move.coord)
                    self.static_items.append(stat_item)
                    self.scene.addItem(stat_item)
                                          
                    #next_positions[ self.coord_straight[pos] ] = ([ self.coord_straight[pos] for pos in poses[0] ], poses[1])

                #next_positions = [ (self.coord_straight[pos[0]], [ self.coord_straight(e) for e in pos[1]]) for pos in f.next_moves ]
                #print(self.coord_straight[f.pos])
                item = self.get_item_by_coord( self.coord_straight[f.pos] )
                #print(item)
                #print('f.next_moves')
                #print(f.next_moves)
                #stat_item = StaticItem('fig.png', item.pos())
                #self.static_items.append(stat_item)
                #self.scene.addItem(stat_item)
                

                item.set_next_positions(f.next_moves)

            # GAME OVER
            if len(moves) == 0:
                print('enemy = ' + ritem.color_enemy)
                if ritem.color_enemy == 'b':
                    self.show_message('Игра закончена!', 'Белые выйграли!')
                    self.setWindowTitle('Белые выйграли! Игра закончена!')                   
                else:
                    self.show_message('Игра закончена!', 'Чёрные выйграли!')
                    self.setWindowTitle('Чёрные выйграли! Игра закончена!')  
                                        
                self.mode = 1                  
            #next_positions = self.board.get_next_positions(ritem.color)

        # if self.mode == 4:
        #     if not ritem.contineous:
        #         self.mode = 3                
        #         self.chess_moved(ritem)
        #     else:
        #         delfigs = ritem.hacked
        #         print('delfigs = ' + str(delfigs))
        #         if len(delfigs) > 0:
        #             for move in delfigs:
        #                 print('del figure')
        #                 item = self.get_item_by_coord( move )
        #                 if item:
        #                     self.get_out_item(item)


 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = Shashki()
    s.show()

    sys.exit(app.exec_())