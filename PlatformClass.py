import pygame
import random
pygame.init()  
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

class Platform:
    def __init__(self,posX,posY,r,g,b):
        self.posX = posX
        self.posY = posY
        self.r = r
        self.g = g
        self.b = b
    def draw(self):
        pygame.draw.rect(screen,(self.r,self.g,self.b),((self.posX,self.posY),(75,25)))
    def Collision(self, x, y):
         pass

platforms = []

platformNum = 5
for i in range(platformNum):
    distance = (800 / platformNum)
    ranx = random.randint(((i * distance) + 10),((i * distance) + 80))
    rany = random.randint(((i * distance) + 10),((i * distance) + 80))
    platforms.append(Platform(ranx,rany,(i + 1)*20, (i + 1)* 25, (i + 1)* 15))

#player variables
xpos = 750 #xpos of player
ypos = 775 #ypos of player
vx = 0 #x velocity of player
vy = 0 #y velocity of player
keys = [False, False, False, False] #this list holds whether each key has been pressed
isOnGround = False #this variable stops gravity from pulling you down more when on a platform
playerHeight = 50
playerWidth = 25

while not gameover:
    clock.tick(60) #FPS
    
    for event in pygame.event.get(): #quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True
      
        if event.type == pygame.KEYDOWN: #keyboard input
            if event.key == pygame.K_a:
                keys[LEFT]=True
            elif event.key == pygame.K_d:
                keys[RIGHT]=True
            elif event.key == pygame.K_w:
                keys[UP]=True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                keys[LEFT]=False
            elif event.key == pygame.K_d:
                keys[RIGHT]=False
            elif event.key == pygame.K_w:
                keys[UP]=False
          

    #LEFT MOVEMENT
    if keys[LEFT]==True:
        vx=-3
        direction = LEFT
    #RIGHT MOVEMENT
    elif keys[RIGHT] == True:
        vx = 3
        direction = RIGHT
    #turn off velocity
    else:
        vx = 0
        #JUMPING
    if keys[UP] == True and isOnGround == True: #only jump when on the ground
        vy = -8
        isOnGround = False
        direction = UP
    
    
        
    xpos+=vx #update player xpos
    ypos+=vy
    
    #COLLISION
    
    #collision with feetsies
    for i in platforms:
        if (((ypos + playerHeight) == i.posY) and (xpos == i.posX)) or (((ypos + playerHeight) == i.posY) and ((xpos + playerWidth) == i.posX + 75)):
            vy = 0
            ypos = i.posY - playerHeight - 1
        if (((ypos + playerHeight) == i.posY) and (xpos == i.posX)) or (((ypos + playerHeight) == i.posY) and ((xpos + playerWidth) == i.posX + 75)):
            vy = 0
            ypos = i.posY - playerHeight - 1

    #stop moving if you hit edge of screen (will be removed for scrolling)
    if xpos+playerWidth > 800:
        xpos-=3
    if xpos<0:
        xpos+=3

    
    #stop falling if on bottom of game screen
    if ypos > 800-playerHeight:
        isOnGround = True
        vy = 0
        ypos = 800-playerHeight
    
    #gravity
    if isOnGround == False:
        vy+=.2 #notice this grows over time, aka ACCELERATION
    


    # RENDER--------------------------------------------------------------------------------
    # Once we've figured out what frame we're on and where we are, time to render.
            
    screen.fill((0,0,0)) #wipe screen so it doesn't smear

    
    for Platform in platforms:
        Platform.draw()
    pygame.draw.rect(screen, (255,0,0), (xpos, ypos, 25,50))
        
    pygame.display.flip()#this actually puts the pixel on the screen
    
#end game loop------------------------------------------------------------------------------
pygame.quit()

