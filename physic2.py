#make a physics demonstration with a brick and a platform
#the brick is affected by gravity and can be moved by the user
import pygame
from pygame.locals import *
import math
import pickle as pk

pygame.init()
WIDTH,HEIGHT=1200,700
win=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Physics Demo")
clock=pygame.time.Clock()
level=pk.load(open("level.dat","rb"))
d={"land":1,"water":2,"air":0}
acid = pygame.Surface((WIDTH, HEIGHT))
acid.fill((0, 255, 0))
acid.set_alpha(60)

camX, camY = 0, 0
robot = pygame.image.load("ROBOT.png")

MW, MH = 3, 2
map = []
for i in range(0, MH):
    mapX = []
    for j in range(0, MW):
        ni = str(i)
        nj = str(j)
        if len(ni) == 1:
            ni = '0' + ni
        if len(nj) == 1:
            nj = '0' + nj
        mapX.append(pygame.image.load("lvls/" + ni + nj + ".png"))
    map.append(mapX)




class Player:
    def __init__(self,x,y,width,height):
        self.x,self.y,self.width,self.height=x,y,width,height
        self.vel=[0,0]
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.y_momentum=0
        self.air_timer=0
    
    def draw(self,win):
        win.blit(robot, (self.rect.x - camX - 15, self.rect.y - camY - 15))

    def physics(self):
        self.vel=[0,0]
        key=pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.vel[0]-=5
        if key[pygame.K_RIGHT]:
            self.vel[0]+=5
        self.vel[1]+=self.y_momentum
        self.y_momentum+=0.2
        if self.y_momentum>8:
            self.y_momentum=8
        collisions=self.move()
        if collisions['bottom']:
            self.y_momentum = 0
            self.air_timer = 0
        else:
            self.air_timer += 1
    
    def move(self):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.x+=self.vel[0]
        pos=[self.rect.x//50,self.rect.y//50]
        blocks=self.returnBlocks(pos)
        hit_list=[]
        for block in blocks:
            if self.rect.colliderect(block):
                hit_list.append(block)
        for tile in hit_list:
            if self.vel[0] > 0:
                self.rect.right = tile.left
                collision_types['right'] = True
            elif self.vel[0] < 0:
                self.rect.left = tile.right
                collision_types['left'] = True
        
        self.rect.y+=self.vel[1]
        pos=[self.rect.x//50,self.rect.y//50]
        blocks=self.returnBlocks(pos)
        hit_list=[]
        for block in blocks:
            if self.rect.colliderect(block):
                hit_list.append(block)

        for tile in hit_list:
            if self.vel[1] > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif self.vel[1] < 0:
                self.rect.top = tile.bottom
                collision_types['top'] = True
                self.y_momentum=0
        return collision_types
    
    def returnBlocks(self,pos):
        blocks=[]
        try:
            if level[pos[1]][pos[0]]==d["land"]:
                blocks.append(pygame.Rect(pos[0]*50,pos[1]*50,50,50))
        except:
            pass
        try:
            if level[pos[1]][pos[0]+1]==d["land"]:
                blocks.append(pygame.Rect((pos[0]+1)*50,pos[1]*50,50,50))
        except:
            pass
        try:
            if level[pos[1]+1][pos[0]]==d["land"]:
                blocks.append(pygame.Rect(pos[0]*50,(pos[1]+1)*50,50,50))
        except:
            pass
        try:
            if level[pos[1]+1][pos[0]+1]==d["land"]:
                blocks.append(pygame.Rect((pos[0]+1)*50,(pos[1]+1)*50,50,50))
        except:
            pass
        return blocks
        # pygame.draw.rect(win,(255,0,0),self.hitbox,2)
player=Player(400,200,50,50)
def drawMap():
    mX = camX // WIDTH
    mY = camY // HEIGHT
    shiftX = camX % WIDTH
    shiftY = camY % HEIGHT
    if mY >= 0 and mY < len(map) and mX >= 0 and mX < len(map[0]):
        win.blit(map[mY][mX], (-shiftX, -shiftY))
    mY += 1
    if mY >= 0 and mY < len(map) and mX >= 0 and mX < len(map[0]):
        win.blit(map[mY][mX], (-shiftX, HEIGHT-shiftY))
    mX += 1
    if mY >= 0 and mY < len(map) and mX >= 0 and mX < len(map[0]):
        win.blit(map[mY][mX], (WIDTH-shiftX, HEIGHT-shiftY))
    mY -= 1
    if mY >= 0 and mY < len(map) and mX >= 0 and mX < len(map[0]):
        win.blit(map[mY][mX], (WIDTH-shiftX, -shiftY))
    
cnt = 0

def update():
    global cnt
    win.fill((0,0,0))
    drawMap()
    player.physics()
    global camX, camY
    camX = player.rect.x - WIDTH // 2
    camY = player.rect.y - HEIGHT // 2
    player.draw(win)
    win.blit(acid, (0, 550 + math.sin(cnt/20) * 10 - camY))
    pygame.draw.rect(win, (0, 255, 0), (0, 550 + math.sin(cnt/20) * 10 - camY, WIDTH, 5))
    pygame.display.update()
    cnt += 1

while True:
    clock.tick(60)
    update()
    for event in pygame.event.get():
        if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
            pygame.quit()
            quit()
        if event.type==KEYDOWN:
            if event.key==K_SPACE:
                if player.air_timer<6:
                    player.y_momentum=-8
