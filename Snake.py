import pygame
import random
import math
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(250,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0]+self.dirnx, self.pos[1]+self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    #to know in which way the snake is turning
                    

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
             p = c.pos[:] # for each cube in the body, see if it's at turn pos
             if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:#if the cube if the last cube
                    self.turns.pop(p)#remove the turn
             else:
                     #check whether reach the bound of the screen
                     if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                     elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                     elif c.dirny ==1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0],0)
                     elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                     else: c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
#addCube
        if dx == 1 and dy == 0:
           self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
#move the cube
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def minCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
#minCube
        self.body.pop(-1)


    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface,True)
            else:
                c.draw(surface)
    
def drawGrid(w, r, surface):
    sizeBtwn = w // r;

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface,(255,255,255), (x,0),(x,w))#start and end position of line
        pygame.draw.line(surface,(255,255,255), (0,y),(w,y))#(255,255,255) is the color
        

def redrawWindow(surface):#surface is the screen buffer
    global rows, width, s, snake
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    unsafe_food.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnake(rows,item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:#check if the pos is on the snake
            continue
        else:
            break

    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack, unsafe_food
    width = 500
    rows = 20
    surface = pygame.display.set_mode((width,width)) #Initialize a window or screen for display
    s = snake((255,0,0),(10,10))
    snack = cube(randomSnake(rows, s), color = (0,255,0))
    unsafe_food = cube(randomSnake(rows, s), color = (255,215,0))
    flag = True

    clock = pygame.time.Clock()
    
    while flag:
        pygame.time.delay(50) #pause the snake for an amount of time, higher slower
        clock.tick(10) #This can be used to help limit the runtime speed of a game.the program will never run at more than 10 frames per second.
        #snake is moving 10 block per millisec
        s.move()
        if s.body[0].pos == snack.pos:#if snake ate the snack, addCube
            s.addCube()
            snack = cube(randomSnake(rows, s), color = (0,255,0))
        if s.body[0].pos == unsafe_food.pos:#if snake ate the unsafe_food, minusCube
            s.minCube()
            unsafe_food = cube(randomSnake(rows, s), color = (255,215,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box("You lost!", "Play again")
                m.reset((10,10))
                break
            
        redrawWindow(surface)
main()
        
