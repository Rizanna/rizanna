import pygame
import random

pygame.init()

screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("SNAKE")
backgroundimage=pygame.image.load('pole.png')
foodImage = pygame.image.load("carrot.png")

class Snake:
    def __init__(self):
        self.size = 1 #колво элементов
        self.elements = [[100,100]] #координаты змейки
        self.radius = 10
        self.dx = 5   #right
        self.dy = 0
        self.is_add = False
        self.score = 0
    def draw(self):
        for element in self.elements:
            pygame.draw.circle(screen, (255, 0, 0),element,self.radius)

    def add_to_snake(self):
        self.size += 1
        self.elements.append([0, 0]) #примыкают к посл элементу
        self.is_add = False

    def move(self):
        if self.is_add:
            self.add_to_snake()
            # size = 5
        for i in range(self.size-1, 0, -1):#пробегаемсяскнца(сайз-1)до 0(невкл)шагом -1
            self.elements[i][0] = self.elements[i - 1][0] #i=4элемент
            self.elements[i][1] = self.elements[i - 1][1] #4элем взял значение 3го
        
        self.elements[0][0] += self.dx  #меняемголову
        self.elements[0][1] += self.dy


class Food:
    def __init__(self):
        self.x = random.randint(15,540)
        self.y = random.randint(15,540)


    def draw(self):
        screen.blit(foodImage,(self.x, self.y))

def Encounter():
     if (food.x>= snake.elements[0][0]-15 and food.x<snake.elements[0][0]+15) and  (food.y >= snake.elements[0][1] - 15 and food.y<snake.elements[0][1] + 15):
        snake.is_add = True  
        if snake.is_add == True:
            snake.score +=1
            food.x = random.randint(10, 550)
            food.y = random.randint(10, 450)
def Scores():
    font = pygame.font.SysFont("Impact", 35)
    score = font.render("S C O R E: " + str(snake.score), True, (255,0,0))
    screen.blit(score, (430,20))





snake = Snake()
food = Food()
running = True
score = 0
d = 5

FPS = 30

clock = pygame.time.Clock()

k1_pressed = False

while running:
    mill = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_RIGHT:
                snake.dx = d #по иксу растет
                snake.dy = 0
            if event.key == pygame.K_LEFT:
                snake.dx = -d
                snake.dy = 0
            if event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -d
            if event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = d
    


    screen.blit(backgroundimage, (0, 0))  

   
              
    snake.move()
    Encounter()
    
    snake.draw()
    food.draw()
    Scores()
    pygame.display.flip()


