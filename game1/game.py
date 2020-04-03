import pygame
import random
pygame.init()

screen = pygame.display.set_mode((600,700))

def inter(x1,y1,x2,y2,db1,db2):
    if x1>x2-db1 and x1<x2+db2 and y1>y2-db1 and y1<y2+db2:
        return 1
    else:
        return 0
clock = pygame.time.Clock()
done = False # игра не закончилась
backgroundImage = pygame.image.load("background1.png")
playerImage = pygame.image.load("raketa.png")
player_x = 200
player_y = 600

bulletImage=pygame.image.load("pulya.png")

enemyImage = pygame.image.load("vrag.png")
enemy_x = random.randint(0,636)
enemy_y = random.randint(20, 50)

enemy_dx = 10
enemy_dy = 10

bullet_x = player_x
bullet_y = player_y

def player(x,y):
    screen.blit(playerImage, (x, y))

def enemy(x,y):
    screen.blit(enemyImage, (x, y))

def bullet(x,y):
    screen.blit(bulletImage,(x,y))

count = 0
myfont = pygame.font.SysFont('monospace',30)
while not done:
    for event in pygame.event.get(): # this empties the event queue
        # event on quit
        if event.type == pygame.QUIT:   #игразакончится
                done = True
        
    
    pressed = pygame.key.get_pressed() # Массив всех нажатых кнопок
  
    if pressed[pygame.K_LEFT]:
         player_x -= 10
         bullet_x = player_x
    if pressed[pygame.K_RIGHT]:
         player_x += 10
         bullet_x = player_x


    screen.fill((0,0,0))

    bullet_y-=40
    if bullet_y < 0 or bullet_y == enemy_y:
        bullet_y = player_y
    if bullet_y < player_y:
        bullet_x = player_x
    
    enemy_x += enemy_dx
    if enemy_x < 0 or enemy_x > 636:
        enemy_dx = -enemy_dx  #меняем направление
        enemy_y += enemy_dy

    if inter(bullet_x,bullet_y,enemy_x,enemy_y,20,50):
        count+=1
    
    string = myfont.render('SCORE:'+ str(count),0,(255,255,255))
    

    screen.blit(backgroundImage,(0, 0))
    player(player_x,player_y)
    bullet(player_x,player_y)
    enemy(enemy_x,enemy_y)
    screen.blit(string,(0, 0))
    bullet(bullet_x,bullet_y)
    clock.tick(20)
    pygame.display.flip()
    