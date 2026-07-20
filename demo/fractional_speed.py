import pygame
import time

class Speed:
    def __init__(self, pixels, time):
        self.pixels = pixels
        self.time = time
    def incr(self):
        if self.time > 1:
            self.time -= 1
        else:
            self.pixels += 1
    def decr(self):
        if self.pixels > 1:
            self.pixels -= 1
        else:
            self.time += 1

win = pygame.display.set_mode((160, 160))

pos = 0

speed = Speed(1, 10)
clock = pygame.time.Clock()

run = True
tick = 0
while run:
    clock.tick(60) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                speed.incr()
            if event.key == pygame.K_DOWN:
                speed.decr()

    win.fill((0,0,0))

    if tick % speed.time == 0:
        pos += speed.pixels
    
    if pos > 160: pos = -32

    pygame.draw.rect(win, (255, 255, 255), (pos, 0, 16, 512))
    pygame.display.update()
    tick += 1

    print(f"Speed: {speed.pixels/speed.time} pixels per frame")


