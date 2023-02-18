import pygame
from pygame.locals import *
import pickle as pk

WIDTH,HEIGHT=1200,700
pygame.init()
win=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Image Loader")
clock=pygame.time.Clock()

fptr = open("level.dat", "rb")
grid = pk.load(fptr)
fptr.close()

tiles = []
for i in range(0, 10):
    tiles.append(pygame.image.load("tiles/t3" + str(i) + ".png"))

def drawFrame(surf, sx, sy):
    gy = sy
    for y in range(0, HEIGHT, 50):
        gx = sx
        for x in range(0, WIDTH, 50):
            if gy < len(grid) and gx < len(grid[0]) and grid[gy][gx] > 0:
                type = 0
                cnt = 0
                cnt += (grid[gy+1][gx] > 0)
                cnt += (grid[gy-1][gx] > 0)
                cnt += (grid[gy][gx-1] > 0)
                cnt += (grid[gy][gx+1] > 0)
                if cnt == 0:
                    type = 9
                elif cnt == 2:
                    if(grid[gy+1][gx] and grid[gy][gx-1]):
                        type = 2
                    elif(grid[gy][gx-1] and grid[gy-1][gx]):
                        type = 8
                    elif(grid[gy-1][gx] and grid[gy][gx+1]):
                        type = 6
                    else:
                        type = 0
                elif cnt == 3:
                    if(not grid[gy+1][gx]):
                        type = 7
                    elif(not grid[gy-1][gx]):
                        type = 1
                    elif(not grid[gy][gx-1]):
                        type = 5
                    else:
                        type = 3
                else:
                    if(not grid[gy+1][gx+1]):
                        type = 0
                    elif(not grid[gy-1][gx-1]):
                        type = 8
                    elif(not grid[gy-1][gx+1]):
                        type = 6
                    elif(not grid[gy+1][gx-1]):
                        type = 2
                    else:
                        type = 4
                surf.blit(tiles[type], (x, y))

            gx += 1
        gy += 1


def update(x, y):
    bg = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
    bg = bg.convert_alpha()
    drawFrame(bg, x, y)
    win.fill((255, 255, 255))
    win.blit(bg, (0, 0))
    pygame.display.update()
    namey = str(y*50 // HEIGHT)
    namex = str(x*50 // WIDTH)
    if len(namey) == 1:
        namey = '0' + namey
    if len(namex) == 1:
        namex = '0' + namex
    pygame.image.save(bg, "lvls/" + namey + namex + ".png")

y = 0
while(y < len(grid)):
    x = 0
    while(x < len(grid[0])):
        clock.tick(2)
        update(x, y)
        x += WIDTH//50
    y += HEIGHT//50
