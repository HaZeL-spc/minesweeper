import pygame
import random
import os

dirname = os.path.dirname(__file__)

pygame.init()

win_width = 800
win_height = 800
tile_width = 80
how_many_bombs = 10

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

number_colors = [(0,0,255),	(0,128,0),(255,0,0),(0,0,128),(128,0,0),(0,128,128),(0,0,0),(128,128,128)]
white = (255,255,255)
bg_color = (205,205,205)
red = (255,0,0)
text_color = (0,124,144)

bomb_image = pygame.image.load(os.path.join(dirname,r'png\bomb.png'))
bomb_image = pygame.transform.scale(bomb_image, (tile_width, tile_width))
flag_icon = pygame.image.load(os.path.join(dirname,r'png\Flag_icon.svg'))
flag_icon = pygame.transform.scale(flag_icon, (int(tile_width*0.6), int(tile_width*0.8)))
brighten = 54
flag_icon.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 

class Tile:
    def __init__(self, x, y, width, height, is_bomb, color, clickedBomb, clickedFlag, showed, licznik,expected):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_bomb = is_bomb
        self.color = color
        self.clickedBomb = clickedBomb
        self.clickedFlag = clickedFlag
        self.showed = showed
        self.freeField = True
        self.licznik = licznik
        self.expected = expected

def randomBombs(clicked):
    global bombs
        
    possibilities = [i for i in range(win_width//tile_width*10)]
    if clicked != None:
        possibilities.pop(possibilities.index(clicked[0]//tile_width + clicked[1]//tile_width*10))

    for i in range(how_many_bombs):
        choice = random.choice(possibilities)
        possibilities.pop(possibilities.index(choice))
        x = choice % (win_width//tile_width)
        y = choice // (win_height//tile_width)

        bombs.append([x*tile_width,y*tile_width])  

def setupTiles():
    global tiles
    for y in range(win_height//tile_width):
        for x in range(win_width//tile_width):
            is_bomb_tile = False
            for bomb in bombs:
                if x*tile_width == bomb[0] and y*tile_width == bomb[1]:
                    is_bomb_tile = True
                    break
            if is_bomb_tile:
                 tiles.append(Tile(x*tile_width, y*tile_width, tile_width, tile_width, True, bg_color, False, False))
            else:
                 tiles.append(Tile(x*tile_width, y*tile_width, tile_width, tile_width, False, bg_color, False, False))

def restartGame(restart,win,clicked):
    global bombs 
    global tiles
    global end_game
    global flag_elements
    global first_click

    bombs = []
    tiles = []
    if restart:
        i = 0
        redrawGameWindow(win)
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
                    run = False 

        end_game = False
    flag_elements = []
    first_click = True
    randomBombs(clicked)
    for y in range(win_height//tile_width):
        for x in range(win_width//tile_width): 
            info = checkNeighbour(win_width//tile_width, x, y)
            x_start = info[0]
            x_barrier = info[1]
            x_dir = info[2]
            y_start = info[3]
            y_barrier = info[4]
            y_dir = info[5]

            licznik_bomb = 0
            for j in range(y_start, y_barrier, y_dir):
                for i in range(x_start, x_barrier, x_dir):
                    for bomb in bombs:
                        if bomb[0] == i*tile_width and bomb[1] == j*tile_width:
                            licznik_bomb += 1
            
            is_bomb_tile = False
            for bomb in bombs:
                if x*tile_width == bomb[0] and y*tile_width == bomb[1]:
                    is_bomb_tile = True
                    break
            if is_bomb_tile:
                tiles.append(Tile(x*tile_width, y*tile_width, tile_width, tile_width, True, bg_color, False,False,False,None,False))
            else:
                tiles.append(Tile(x*tile_width, y*tile_width, tile_width, tile_width, False, bg_color, False,False, False, licznik_bomb,False))
            

def checkNeighbour(barrier, x, y): 
    if x - 1 >= 0 and x + 1 < barrier:
        dlugosc_x = 3
    else:
        dlugosc_x = 2
    if y - 1 >= 0 and y + 1 < barrier:
        dlugosc_y = 3
    else:
        dlugosc_y = 2

    x_start = x
    y_start = y
    y_dir = 1
    if y == 0:
        if x == 0:
            x_barrier = x + dlugosc_x
            x_dir = 1
            y_barrier = y + dlugosc_y
            y_dir = 1
        elif x == 9:
            x_barrier = x - dlugosc_x
            x_dir = -1
            y_barrier = y + dlugosc_y
            y_dir = 1
        else:
            x_start = x-1
            x_barrier = x-1+dlugosc_x
            x_dir = 1
            y_barrier = y+dlugosc_y
    elif y == 9:
        if x == 0:
            x_barrier = x + dlugosc_x
            x_dir = 1
            y_barrier = y - dlugosc_y
            y_dir = -1
        elif x == 9:
            x_barrier = x - dlugosc_x
            x_dir = - 1
            y_barrier = y - dlugosc_y
            y_dir = -1
        else:
            x_start = x-1
            x_barrier = x-1 + dlugosc_x
            x_dir = 1
            y_barrier = y - dlugosc_y
            y_dir = -1
    elif x == 0:
        x_start = x
        x_barrier = x + dlugosc_x
        x_dir = 1
        y_start = y - 1
        y_barrier = y - 1 + dlugosc_y
        y_dir = 1
    elif x == 9:
        x_start = x - dlugosc_x + 1
        x_barrier = x + 1
        x_dir = 1
        y_start = y-1
        y_barrier = y-1 + dlugosc_y
        y_dir = 1
    else:
        x_start = x-1
        x_barrier = x - 1+dlugosc_x
        x_dir = 1
        y_start = y - 1
        y_barrier = y - 1 + dlugosc_y
        y_dir = 1

    return [x_start, x_barrier, x_dir, y_start, y_barrier, y_dir]

def loadMap():
    for y in range(win_height//tile_width):
        for x in range(win_width//tile_width): 
            tiles.append(Tile(x*tile_width, y*tile_width, tile_width, tile_width, False, bg_color, False,False, False, 0,False))

def showFields(tile):
    x_guess = tile.x
    y_guess = tile.y
    info = checkNeighbour(win_width//tile_width, x_guess//tile_width, y_guess//tile_width)
    x_start = info[0]
    x_barrier = info[1]
    x_dir = info[2]
    y_start = info[3]
    y_barrier = info[4]
    y_dir = info[5]

    is_next_to = False
    for bomb in bombs:
        if (bomb[0] - tile_width == x_guess or bomb[0] + tile_width == x_guess or bomb[0] == x_guess):
            if (bomb[1] - tile_width == y_guess or bomb[1] + tile_width == y_guess or bomb[1] == y_guess):
                is_next_to = True
                tile.showed = True
                if not tile.expected:
                    tile.color = white
                    tile.freeField = False
                break

    if not is_next_to:
        for j in range(y_start, y_barrier, y_dir):
            for i in range(x_start, x_barrier, x_dir):    
                if not tiles[i+j*10].expected: 
                    tiles[i+j*10].showed = True
                    tiles[i+j*10].color = white
                    tiles[i+j*10].freeField = False


def writeText(tile):
    font = pygame.font.SysFont('comicsans', 90)
    if tile.licznik != 0 and tile.licznik != None:
        text = font.render(str(tile.licznik), 1, number_colors[tile.licznik-1])
        win.blit(text, (tile.x + tile.width/2-text.get_width()/2, tile.y + tile.height/2-text.get_height()/2))

def writeScore():
    font = pygame.font.SysFont('comicsans', 40)
    text1 = font.render("pozostałe flagi: ", 1, text_color)
    text2 = font.render(str(how_many_bombs - len(flag_elements)), 1, text_color)
    win.blit(text1, (win_width-text1.get_width()-30,10))
    win.blit(text2, (win_width-text2.get_width()-10,10))

def checkIfWon():
    score_flags = 0
    if len(flag_elements) == how_many_bombs:
        for flag in flag_elements:
            for bomb in bombs:
                if bomb[0] == flag.x and bomb[1] == flag.y:
                    score_flags += 1
                    break
    else:
        score_flags = 100
        for tile in tiles:
            if not tile.is_bomb and tile.showed:
                score_flags -= 1

    print(score_flags)
    if score_flags == how_many_bombs:
        restartGame(True, True,None)

def redrawGameWindow(did_win):
    for tile in tiles:
        pygame.draw.rect(win, tile.color, (tile.x,tile.y,tile.width,tile.height))
        pygame.draw.rect(win, (0,0,0), (tile.x,tile.y,tile.width,tile.height), 1)
        if tile.showed:
            if tile.is_bomb and end_game:
                win.blit(bomb_image,(tile.x,tile.y))
            if not tile.expected:
                writeText(tile)
            else:
                win.blit(flag_icon, (tile.x + tile_width//5, tile.y + tile_width // 10))
    if did_win:
        font = pygame.font.SysFont('comicsans', 100)
        text = font.render("Wygrałeś ", 1, (0,0,0))
        win.blit(text, (win_width//2 - text.get_width()//2,win_height//2 - text.get_height()))
    writeScore()
    pygame.display.update()

bombs = []
tiles = []
run = True
end_game = False
flag_elements = []
first_click = True
#restartGame(False,False,None)
loadMap()


while run:
    clock.tick(30)
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        run = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            for tile in tiles:
                if not tile.showed:
                    if event.pos[0] > tile.x and event.pos[0] < tile.x + tile.width:
                        if event.pos[1] > tile.y and event.pos[1] < tile.y + tile.height:
                            tile.color = (125,125,125)
                            tile.clickedBomb = True
        elif event.button == 3:
            tile_x = int(event.pos[0] - event.pos[0] % tile_width) // tile_width
            tile_y = int(event.pos[1] - event.pos[1] % tile_width) // tile_width
            element = tiles[tile_y*10+tile_x]
            if element.freeField:
                if how_many_bombs - len(flag_elements) > 0:
                    element.expected = not element.expected 
                    element.showed = not element.showed
                    if not element.expected:
                        flag_elements.pop(flag_elements.index(element))
                    else:
                        flag_elements.append(element)
                else:
                    if element.expected:
                        flag_elements.pop(flag_elements.index(element))
                        element.showed = not element.showed

            checkIfWon()

    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            for tile in tiles:
                if tile.clickedBomb:
                    if event.pos[0] > tile.x and event.pos[0] < tile.x + tile.width and event.pos[1] > tile.y and event.pos[1] < tile.y + tile.width:
                        if first_click:
                            tile_copied = tile
                            restartGame(False,False,(tile.x,tile.y))
                            first_click = False
                            tile = tiles[tile_copied.y//tile_width*10+tile_copied.x//tile_width]
                            showFields(tile)
                            break
                        elif not tile.is_bomb:
                            if not tile.expected:
                                showFields(tile)
                                checkIfWon()
                            else:
                                tile.color = bg_color
                        else:
                            tile.color = red
                            for tile in tiles:
                                tile.showed = True
                            end_game = True
                            redrawGameWindow(False)   
                            restartGame(True,False,None)
                    else:
                        tile.color = bg_color

                    tile.clickedBomb = False
    

    redrawGameWindow(False)   

pygame.quit()
