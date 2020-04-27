import pygame
import random
from enum import Enum

pygame.init()

screen = pygame.display.set_mode((800, 600))

backgroundsound = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play()

hitSound =pygame.mixer.Sound('hit.wav')


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Tank:
    def __init__(self, x, y, speed, color, fire,   d_right = pygame.K_RIGHT, d_left = pygame.K_LEFT, d_up = pygame.K_UP, d_down = pygame.K_DOWN):
        self.x = x
        self.y = y
        self.width = 50
        self.lives = 3
        self.speed = speed
        self.color = color
        self.direction = Direction.RIGHT
        self.KEYUP = fire

        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,

                    d_up: Direction.UP, d_down: Direction.DOWN}


    def draw(self):
        tank_c = (self.x + self.width // 2, self.y + self.width // 2)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width), 10)
        pygame.draw.circle(screen, self.color, tank_c, self.width // 2)

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width + self.width // 2, self.y + self.width // 2), 4)
        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (self.x - self.width // 2, self.y + self.width // 2), 4)
        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width // 2, self.y - self.width // 2), 4)
        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width // 2, self.y + self.width + self.width // 2), 4)

    def stay_in_frame(self):
        if self.x < 0 or self.x > screen.get_size()[0]:
            self.x = (self.x + 800) % 800
        if self.y < 0 or self.y > screen.get_size()[1]:
            self.y = (self.y + 600) % 600

    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed
        self.draw()



class Bullet:
    def __init__(self, bullet_x = 0, bullet_y = 0, bullet_color = (0, 0, 0), direction = 'RIGHT', bullet_speed = 10):
        self.bullet_x = bullet_x
        self.bullet_y = bullet_y
        self.bullet_color = bullet_color
        self.bullet_speed = bullet_speed
        self.direction=direction

    def draw_bullet(self):
        pygame.draw.circle(screen, self.bullet_color, (self.bullet_x, self.bullet_y), 10)

    def move_bullet(self):
        if self.direction == Direction.LEFT:
            self.bullet_x -= self.bullet_speed
            
        if self.direction == Direction.RIGHT:
            self.bullet_x += self.bullet_speed

        if self.direction == Direction.UP:
            self.bullet_y -= self.bullet_speed

        if self.direction == Direction.DOWN:
            self.bullet_y += self.bullet_speed

        self.draw_bullet()


def bullet_shoot(tank):
    if tank.direction == Direction.RIGHT:
        bullet_x = tank.x + tank.width + tank.width // 2
        bullet_y = tank.y + tank.width // 2

    if tank.direction == Direction.LEFT:
        bullet_x = tank.x - tank.width // 2
        bullet_y = tank.y + tank.width // 2

    if tank.direction == Direction.UP:
        bullet_x = tank.x + tank.width // 2
        bullet_y = tank.y - tank.width // 2

    if tank.direction == Direction.DOWN:
        bullet_x = tank.x + tank.width // 2
        bullet_y = tank.y + tank.width + tank.width // 2

    bul = Bullet(bullet_x, bullet_y, (0, 0, 0), tank.direction)
    bullets.append(bul)


tank1 = Tank(100, 200, 2, (255, 255,0), pygame.K_RETURN)
tank2 = Tank(300 , 100 , 2 , (255 , 0 , 255),pygame.K_SPACE, 
pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)

bullet1 = Bullet()
bullet2 = Bullet()

tanks = [tank1, tank2]

bullets = [bullet1, bullet2]


game = True

FPS = 60

clock = pygame.time.Clock()


while game:
    millis = clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game = False

            pressed = pygame.key.get_pressed()

            for tank in tanks:
                if event.key in tank.KEY.keys():
                    tank.change_direction(tank.KEY[event.key])        
                if pressed[tank.KEYUP]:
                    bullet_shoot(tank)

        
    screen.fill((255, 255, 255))

    for tank in tanks:                   
        tank.move()
        

    for bul in bullets:
        bul.move_bullet()

    for tank in tanks:
        tank.draw() 

    for tank in tanks:
        tank.stay_in_frame()


    for bul in bullets:
        if bul.bullet_x in range(tanks[0].x , tanks[0].x + 40) and bul.bullet_y in range(tanks[0].y , tanks[0].y + 40): 
            tanks[0].lives -= 1
            bullets.remove(bul)
            hitSound.play()
        if bul.bullet_x in range(tanks[1].x , tanks[1].x + 40) and bul.bullet_y in range(tanks[1].y , tanks[1].y + 40): 
            tanks[1].lives -= 1
            bullets.remove(bul)
            hitSound.play()

        if tanks[0].lives == 0 or tanks[1].lives == 0:
            game = False
            font = pygame.font.SysFont('Arial', 80)
            text = font.render('Game Over', True, (0, 0, 0))
            place = text.get_rect(center=(400, 275))
            screen.blit(text, place)

            if tanks[0].lives == 0:
                font2 = pygame.font.SysFont("Arial", 40)
                text2 = font2.render('TANK1 Wins', True, (255,0,255))
                place2 = text2.get_rect(center=(400, 325))
                screen.blit(text2, place2)

            if tanks[1].lives == 0:
                font3 = pygame.font.SysFont("Arial", 40)
                text3 = font3.render('TANK2 Wins', True, (255 , 255 , 0))
                place3 = text3.get_rect(center=(400, 500))
                screen.blit(text3, place3)


            pygame.display.flip()
            pygame.time.delay(2000)

            continue



    

    pygame.display.flip()



pygame.quit()