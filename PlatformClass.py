from math import cos, sin
import pygame
import random
pygame.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
pygame.display.set_caption("Platform Classes")  # sets the window title
screen = pygame.display.set_mode((800, 800))  # creates game screen
screen.fill((0,0,0))
clock = pygame.time.Clock() #set up clock
gameover = False #variable to run our game loop

#CONSTANTS
LEFT=0
RIGHT=1
UP = 2
DOWN = 3

class Player:
    def __init__(self):
        self.LEFT = 0
        self.RIGHT = 1
        self.UP = 2
        self.DOWN = 3
        
        self.xpos = 400
        self.ypos = 775
        self.vy = 0
        
        self.keys = [False, False, False, False]
        
        self.isOnGround = False
        self.playerHeight = 25
        self.playerWidth = 25
        self.offset = 0
        self.inputDelay = 0


class Platform:
    def __init__(self,posX,posY,color,movable):
        self.posX = posX
        self.posY = posY
        self.color = color
        self.r = 0
        self.g = 0
        self.b = 0
        self.offset = 0
        self.angle = 0
        self.speed = 1/20
        self.radius = 100
        self.moving = movable
        if self.moving:
            self.shiftX = posX
            self.shiftY = posY

        if self.color == "red\n":
            self.r=250
            self.g=random.randrange(0,250)
            self.b=random.randrange(0,250)
           
        elif self.color == "blue\n":
            self.r=random.randrange(0,250)
            self.g=random.randrange(0,250)
            self.b=250
        elif self.color == "green\n":
            self.r=random.randrange(0,250)
            self.g=250
            self.b=random.randrange(0,250)
        elif self.color == "yellow":
            self.r=random.randrange(150,250)
            self.g=random.randrange(150,250)
            self.b=random.randrange(0,250)
        else:
            self.r = random.randrange(0,250)
            self.g = random.randrange(0,250)
            self.b = random.randrange(0,250)

    def draw(self):
        pygame.draw.rect(screen,(self.r,self.g,self.b),((self.posX + self.offset,self.posY),(75,25)))

    def collide(self, x, y, playerWidth, playerHeight):
        if (x + playerWidth) > (self.posX + self.offset) and x < (self.posX + self.offset + 75) and (y + playerHeight) > (self.posY) and (y) < self.posY + playerHeight:
            return self.posY - playerHeight
        else:
            return False


    def update(self,offset):
        self.offset = offset
        if self.moving == True:
            self.angle += self.speed
            self.posX = self.radius * cos(self.angle) + self.shiftX
            self.posY = self.radius * sin(self.angle) + self.shiftY

def createPlatforms(theColors):
    platforms = list()
    gameColor = theColors[random.randrange(0, len(theColors))]
    for i in range(30):
        move = True if random.randint(0,10) == 1 else False
        platx = random.randrange(-1500,1500,250)
        platy = random.randrange(100,700,100)
        platforms.append(Platform(platx,platy,gameColor,move))
    return platforms

jump = pygame.mixer.Sound('message.wav')
pygame.mixer.Sound.set_volume(jump, .1)
music = pygame.mixer.music.load('music.wav')
pygame.mixer.music.set_volume(.1)
pygame.mixer.music.play(-1)

colors = open("colors.txt", "r")

theColors = list()

for line in colors:
    theColors.append(line)

platforms = createPlatforms(theColors)

player_count = 2
players = []
for i in range(player_count):
    players.append(Player())

while not gameover:
    clock.tick(60) #FPS
    
    for event in pygame.event.get(): #quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True
        
        if event.type == pygame.KEYDOWN: #keyboard input
            if event.key == pygame.K_a:
                players[0].keys[players[0].LEFT]=True
            elif event.key == pygame.K_d:
                players[0].keys[players[0].RIGHT]=True
            elif event.key == pygame.K_w:
                players[0].keys[players[0].UP]=True
                
            if event.key == pygame.K_LEFT:
                players[1].keys[players[1].LEFT]=True
            elif event.key == pygame.K_RIGHT:
                players[1].keys[players[1].RIGHT]=True
            elif event.key == pygame.K_UP:
                players[1].keys[players[1].UP]=True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                players[0].keys[players[0].LEFT]=False
            elif event.key == pygame.K_d:
                players[0].keys[players[0].RIGHT]=False
            elif event.key == pygame.K_w:
                players[0].keys[players[0].UP]=False
                
            if event.key == pygame.K_LEFT:
                players[1].keys[players[1].LEFT]=False
            elif event.key == pygame.K_RIGHT:
                players[1].keys[players[1].RIGHT]=False
            elif event.key == pygame.K_UP:
                players[1].keys[players[1].UP]=False
                
                
        #Not player dependent      
        if event.type == pygame.JOYAXISMOTION: #keyboard input
            if joysticks[0].get_axis(0) < 0:
                keys[LEFT]=True
            else:
                keys[LEFT]=False
            if joysticks[0].get_axis(0) > 0:
                keys[RIGHT]=True
            else:
                keys[RIGHT]=False
            if joysticks[0].get_axis(1) == -1:
                keys[UP]=True
            else:
                keys[UP]=False
        
    
    for i in players:
        if i.ypos <= 0:
            platforms = createPlatforms(theColors)
            i.ypos = 725

        #LEFT MOVEMENT
        if i.keys[i.LEFT]==True:
            i.offset += 8
        #RIGHT MOVEMENT
        elif i.keys[i.RIGHT] == True:
            i.offset += -8
            #JUMPING
        if i.keys[i.UP] == True and i.isOnGround == True: #only jump when on the ground
            pygame.mixer.Sound.play(jump)
            i.vy = -10
            i.isOnGround = False

        i.isOnGround = False
        #collision with feetsies
        for plats in platforms:
            if plats.collide(i.xpos,i.ypos,i.playerWidth,i.playerHeight) != False:
                i.ypos = plats.collide(i.xpos,i.ypos,i.playerWidth,i.playerHeight)
                i.vy = 0
                i.isOnGround = True
        #stop falling if on bottom of game screen
        if i.ypos > 800-i.playerHeight:
            i.isOnGround = True
            i.vy = 0
            i.ypos = 800-i.playerHeight
        
        #gravity
        if i.isOnGround == False:
            i.vy+=.3 #notice this grows over time, aka ACCELERATION
        
        i.ypos+=i.vy
    for plats in platforms:
       plats.update(i.offset)

    # RENDER--------------------------------------------------------------------------------
    # Once we've figured out what frame we're on and where we are, time to render.
            
    screen.fill((0,0,0)) #wipe screen so it doesn't smear

    for plats in platforms:
        plats.draw()
    for i in players:
        pygame.draw.rect(screen, (255,0,0), (i.xpos, i.ypos, i.playerWidth, i.playerHeight))
        i.inputDelay += 1
        
    pygame.display.flip()#this actually puts the pixel on the screen
    
    
    
#end game loop------------------------------------------------------------------------------
pygame.quit()

