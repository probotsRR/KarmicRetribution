#Level editor for the game
#addign numbers with a unique color and 0 is the default color for nothing
import pygame
from pygame.locals import *
import pickle as pk

WIDTH,HEIGHT=1200,700
pygame.init()
win=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Level Editor")
clock=pygame.time.Clock()
#colors
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
ORANGE=(255,165,0)
PURPLE=(128,0,128)
BROWN=(165,42,42)
GREY=(128,128,128)

#current color
current_color=0
flood = False
grid=[[0]*(WIDTH//50) for _ in range(HEIGHT//50-1)]
offset_x,offset_y=0,0
print(len(grid),HEIGHT//50)

#defining the grid
def drawGrid():
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if (click[0]==1):
        x=mouse[0]//50
        y=mouse[1]//50
        if y>=1:
            if not flood:
                grid[y+offset_y-1][x+offset_x]=current_color
            elif grid[y+offset_y-1][x+offset_x]!=current_color:
                floodFill(x+offset_x, y+offset_y-1, grid[y+offset_y-1][x+offset_x])
    color=0
    for i in range(HEIGHT//50-1):
        i+=offset_y
        for j in range(WIDTH//50):
            j+=offset_x
            # print(i,j,len(grid),len(grid[0]))
            if grid[i][j]==0:
                continue
            elif grid[i][j]==1:
                color=BLACK
            elif grid[i][j]==2:
                color=RED
            elif grid[i][j]==3:
                color=GREEN
            elif grid[i][j]==4:
                color=BLUE
            elif grid[i][j]==5:
                color=YELLOW
            elif grid[i][j]==6:
                color=ORANGE
            elif grid[i][j]==7:
                color=PURPLE
            elif grid[i][j]==8:
                color=BROWN
            elif grid[i][j]==9:
                color=GREY
            pygame.draw.rect(win,color,((j-offset_x)*50,(i-offset_y+1)*50,50,50))

    for i in range(0,WIDTH,50):
        pygame.draw.line(win,BLACK,(i,50),(i,HEIGHT))
    for i in range(50,HEIGHT,50):
        pygame.draw.line(win,BLACK,(0,i),(WIDTH,i))

def save():
    #dump the grid into a file level.dat and dump the grid into a file
    fptr = open("level.dat", "wb")
    pk.dump(grid, fptr)
    fptr.close()

def load(file):
    #load the grid from the file
    fptr = open(file, "rb")
    grid = pk.load(fptr)
    fptr.close()
    return grid

#defining the buttons
class Button:
    def __init__(self,rect,color,value):
        self.button=rect
        self.color=color
        self.value=value
    
    def draw(self):
        pygame.draw.rect(win,self.color,self.button)
        if self.value == current_color:
            pygame.draw.rect(win,(0,0,0),self.button,2)
            
    
    def onClick(self):
        global current_color
        global flood
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        if self.button.collidepoint(mouse):
            if click[0]==1 and self.value!=100:
                current_color=self.value
                flood = False
                # print(current_color)
            if click[0]==1 and self.value==100:
                flood = True

def floodFill(x, y, col):
        grid[y][x] = current_color
        if y<len(grid)-1 and grid[y+1][x] == col:
            floodFill(x,y+1,col)
        if y>0 and grid[y-1][x] == col:
            floodFill(x,y-1,col)
        if x<len(grid[0])-1 and grid[y][x+1] == col:
            floodFill(x+1,y,col)
        if x>0 and grid[y][x-1] == col:
            floodFill(x-1,y,col)



buttons=[Button(pygame.Rect((0,0,50,50)),(200,100,100),100),Button(pygame.Rect((50,0,50,50)),WHITE,0),Button(pygame.Rect(100,0,50,50),BLACK,1),Button(pygame.Rect(150,0,50,50),RED,2),Button(pygame.Rect(200,0,50,50),GREEN,3),Button(pygame.Rect(250,0,50,50),BLUE,4),Button(pygame.Rect(300,0,50,50),YELLOW,5),Button(pygame.Rect(350,0,50,50),ORANGE,6),Button(pygame.Rect(400,0,50,50),PURPLE,7),Button(pygame.Rect(400,0,50,50),BROWN,8),Button(pygame.Rect(450,0,50,50),GREY,9)]
def putButtons():
    for button in buttons:
        button.draw()
        button.onClick()

def update():
    # print(len(grid[0]),offset_x)
    win.fill(WHITE)
    drawGrid()
    putButtons()
    pygame.display.update()

while True:
    clock.tick(60)
    update()
    for event in pygame.event.get():
        if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
            pygame.quit()
            quit()
        if event.type==KEYDOWN:
            if event.key==K_s:
                save()
            if event.key==K_o:
                grid=load("level.dat")
            if event.key==K_LEFT:
                if offset_x!=0:
                    offset_x-=1
                else:
                    for i in range(len(grid)):
                        grid[i].insert(0,0)
            if event.key==K_RIGHT:
                if offset_x<len(grid[0])-WIDTH//50:
                    offset_x+=1
                else:
                    offset_x+=1
                    for i in range(len(grid)):
                        grid[i].append(0)
            if event.key==K_UP:
                if offset_y!=0:
                    offset_y-=1
                else:
                    grid.insert(0,[0]*len(grid[0]))
            if event.key==K_DOWN:
                # print(len(grid),HEIGHT//50)
                if offset_y<len(grid)-HEIGHT//50-1:
                    offset_y+=1
                else:
                    offset_y+=1
                    grid.append([0]*len(grid[0]))
                # print(offset_y,len(grid))
