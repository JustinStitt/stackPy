import pygame
import sys
import time
import random
pygame.init()

#Constants
WIDTH = 400
HEIGHT = 800
fps = 60
#end Constants
#setup                           
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('StackPy - Justin Stitt')
clock = pygame.time.Clock()
#end setup
background_color = pygame.Color(42,42,44)

blocks = []

score = 0
gamestate = 0 # 0 = playing, 1 = lost

class Block:
    def __init__(self,new_height = 0,new_width = 0):
        self.height = HEIGHT//16#ratio
        self.width = WIDTH//3#ratio
        self.pos = [0,HEIGHT - self.height]
        if(new_height > 0):
            self.pos[1] = new_height
        if(new_width > 0):
            self.width = new_width
        self.speed = 5
        self.color = pygame.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.rect = [self.pos[0],self.pos[1],self.width,self.height]
        self.genesis = False
        if(len(blocks) == 1):
            self.genesis = True
    def update(self):

        self.pos[0] += self.speed

        self.rect = [self.pos[0],self.pos[1],self.width,self.height]
        self.check_bounds()
        self.render()
    def render(self):
        pygame.draw.rect(screen,self.color,self.rect)
    def check_bounds(self):
        if(self.pos[0] <= 0):
            self.speed *= -1#reverse speed
        elif(self.pos[0] + self.width >= WIDTH):
            self.speed *= -1#reverse speed
    def place(self,index):
        if(index < 0):
            self.speed = 0
            self.new_block()
        else:
            self.speed = 0
            self.slice(index)
            self.new_block()
    def new_block(self):
        if(gamestate == 1):
            return
        new_height = self.pos[1]- self.height
        if(new_height <= self.height):
            print("in")
            for block in blocks:
                block.pos[1] += HEIGHT - self.pos[1] - self.height
            blocks.append(Block(new_height + (HEIGHT - 3*self.height) , self.width))
        else:
            blocks.append(Block(new_height  , self.width))

    def slice(self,index):
        global score, gamestate
        diff = self.pos[0] - blocks[index].pos[0]
        if(self.pos[0] > blocks[index].pos[0] + blocks[index].width or self.pos[0] + self.width < blocks[index].pos[0]):
            for x in range( (score//14) + 1):
                zoom_out()
                gamestate = 1
                blocks[-1].color = [255,0,0]
            return
            #insert zoom out function here
        elif(diff < 0 ):
            self.pos[0] = blocks[index].pos[0]
            self.width += diff
        else:
            self.width -= ( (self.pos[0] + self.width) - (blocks[index].pos[0]+blocks[index].width) )
        score+=1
        print(score)


def zoom_out():
    if(gamestate == 1):
        return
    if(blocks[0].pos[1] > HEIGHT):
        for block in blocks:
            block.pos[1] = (block.pos[1]-HEIGHT + block.height)
    for block in blocks:
        block.width/=2
        block.height/=2
        block.pos[0] /= 2
        block.pos[1] /= 2
        block.pos[0] += WIDTH//4
        block.pos[1] += HEIGHT//2


def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                blocks[-1].place(len(blocks) - 2)
            elif event.key == pygame.K_j:
                print("zooming out!")
                zoom_out()
            elif event.key == pygame.K_k:
                print('blocks 0: {}'.format(blocks[0].pos[1]))
                print(blocks[1].pos[1])
    for block in blocks:
        block.update()

def render():
    pass


blocks.append(Block())#initial block

while True:
    screen.fill(background_color)
    update()
    render()
    pygame.display.flip()
    clock.tick(fps)
