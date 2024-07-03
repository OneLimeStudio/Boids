import pygame
import random
import threading
import math
SCREEN_WIDTH =  1280
SCREEN_HEIGHT = 1080
RADIUS = 3
speedLimit = 8
moveAwayStrength = 1
N = 150
window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


class Boid:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.velocityX = 0
        self.velocityY = 0
        
    
    def draw(self,window):
        pygame.draw.circle(window,(200,0,0), (self.x,self.y), RADIUS)
    
Boids = []


running = True
clock = pygame.time.Clock()

def InitialSpawnBoids():
    for i in range(0,N):
        x = random.randint(RADIUS,SCREEN_WIDTH-RADIUS)
        y = random.randint(RADIUS,SCREEN_HEIGHT-RADIUS)
        
        Boids.append(Boid(x,y))
        


def toCenter(obj):
    com_x = 0
    com_y = 0
    for boid in Boids:
        if boid != obj:
            com_x += boid.x
            com_y += boid.y
    return ((com_x/N-1) - obj.x)/100,((com_y/N-1) - obj.y)/100
            
def keepDistance(obj):
    c_x,c_y = 0,0
    for boid in Boids:
        if boid != obj:
            dist = math.sqrt(   (boid.x-obj.x)**2  + (boid.y-obj.y)**2  )
            if dist < 3*RADIUS:
                c_x -= (boid.x - obj.x)
                c_y -= (boid.y - obj.y)
                
    return c_x,c_y 

def matchVelocity(obj):
    velx,vely = 0,0
    for boid in Boids:
        if obj != boid:
            velx += boid.velocityX
            vely += boid.velocityY
            
    velx /= N-1
    vely /= N-1
    return (velx - obj.velocityX)/8,(vely - obj.velocityY)/8


def movetoSpace(boid,x,y):
    return (x-boid.x)/500,(y - boid.y)/500



def LimitSpeed(boid,Limit):
    if boid.velocityX > Limit:
        boid.velocityX = (boid.velocityX/ abs(boid.velocityX)) *Limit
    if boid.velocityY > Limit:
        boid.velocityY = (boid.velocityY/ abs(boid.velocityY)) *Limit

def boundPosition(boid):
    if boid.x < 0:
        boid.velocityX = 5
    elif boid.x > SCREEN_WIDTH:
        boid.velocityX = -5
    
    if boid.y < 0:
        boid.velocityY = 5
    elif boid.y > SCREEN_HEIGHT:
        boid.velocityY = -5
    
movetoX , movetoY = SCREEN_WIDTH/2,SCREEN_HEIGHT/2    
InitialSpawnBoids()
while running:
    window.fill((0,0,0))
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                moveAwayStrength = -50
                print("Flock Dispersed")
        elif event.type == pygame.MOUSEBUTTONUP:
            movetoX,movetoY = pygame.mouse.get_pos()
    
    for boid in Boids:
        
        LimitSpeed(boid,speedLimit)
        boundPosition(boid)
 
        v1_x,v1_y = toCenter(boid)
        v2_x,v2_y = keepDistance(boid)
        v3_x,v3_y = matchVelocity(boid)
        v4_x , v4_y =movetoSpace(boid,movetoX,movetoY)
        
        
        
        
        boid.velocityX += (v1_x+ v2_x  ) * moveAwayStrength + v3_x+ v4_x
        boid.velocityY += (v1_y+v2_y  ) * moveAwayStrength +  v4_y +v3_y
        
        boid.x += boid.velocityX
        boid.y += boid.velocityY
    
    moveAwayStrength = 1

    for boid in Boids:
        boid.draw(window)
    pygame.display.update()