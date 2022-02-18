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
    def __init__(self,posX,posY,color):
        self.posX = posX
        self.posY = posY
        self.color = color
        self.r = 0
        self.g = 0
        self.b = 0
        self.offset = 0

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


    def collide(self, x, y):
        if (x + playerWidth) > (self.posX + self.offset) and x < (self.posX + self.offset + 75) and (y + playerHeight) > (self.posY) and (y) < self.posY + playerHeight:
            return self.posY - playerHeight
        else:
            return False


    def update(self,offset):
        self.offset = offset

def createPlatforms(theColors):
    platforms = list()
    gameColor = theColors[random.randrange(0, len(theColors))]
    for i in range(30):
        platx = random.randrange(-1500,1500,250)
        platy = random.randrange(100,700,100)
        platforms.append(Platform(platx,platy,gameColor))
    return platforms


colors = open("colors.txt", "r")

theColors = list()

for line in colors:
    theColors.append(line)

platforms = createPlatforms(theColors)
platforms = createPlatforms(theColors)
platforms = createPlatforms(theColors)

#player variables
xpos = 400 #xpos of player
ypos = 775 #ypos of player
vx = 0 #x velocity of player
vy = 0 #y velocity of player
keys = [False, False, False, False] #this list holds whether each key has been pressed
isOnGround = False #this variable stops gravity from pulling you down more when on a platform
playerHeight = 25
playerWidth = 25
offset = 0

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
    
    if ypos <= 0:
        platforms = createPlatforms(theColors)
        ypos = 725

    #LEFT MOVEMENT
    if keys[LEFT]==True:
        offset += 8
    #RIGHT MOVEMENT
    elif keys[RIGHT] == True:
        offset += -8
        #JUMPING
    if keys[UP] == True and isOnGround == True: #only jump when on the ground
        vy = -10
        isOnGround = False

    isOnGround = False
    #collision with feetsies
    for plats in platforms:
        if plats.collide(xpos,ypos) != False:
            ypos = plats.collide(xpos,ypos)
            vy = 0
            isOnGround = True
    #stop falling if on bottom of game screen
    if ypos > 800-playerHeight:
        isOnGround = True
        vy = 0
        ypos = 800-playerHeight
    
    #gravity
    if isOnGround == False:
        vy+=.3 #notice this grows over time, aka ACCELERATION
    
    ypos+=vy
    for plats in platforms:
       plats.update(offset)

    # RENDER--------------------------------------------------------------------------------
    # Once we've figured out what frame we're on and where we are, time to render.
            
    screen.fill((0,0,0)) #wipe screen so it doesn't smear

    for plats in platforms:
        plats.draw()
    pygame.draw.rect(screen, (255,0,0), (xpos, ypos, playerWidth, playerHeight))
        
    pygame.display.flip()#this actually puts the pixel on the screen
    
#end game loop------------------------------------------------------------------------------
pygame.quit()

