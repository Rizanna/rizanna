import pygame
import pika
import sys
import random
import time
from pygame import mixer
from enum import Enum
from threading import Thread
import uuid
import json

IP = '34.254.177.17'
PORT = '5672'
VHOST = 'dar-tanks'
USER = 'dar-tanks'
PSSWRD = '5orPLExUYnyVYZg48caMpX'
ROOM = 'room-1'

pygame.init()


screen = pygame.display.set_mode((800, 600))
foodImage = pygame.image.load("carrot.png")
pygame.display.set_caption("TANK WAR")
backgroundimage=pygame.image.load('back3.jpg')

vzryv_sound = pygame.mixer.music.load("vzryv.wav")
back_sound = pygame.mixer.music.load("backmuz.wav")
pygame.mixer.music.play()
vzryv_sound =pygame.mixer.Sound('vzryv.wav')


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Tank:
    def __init__(self, x, y, speed, color, shot, d_right = pygame.K_RIGHT, d_left = pygame.K_LEFT, d_up = pygame.K_UP, d_down = pygame.K_DOWN):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 50
        self.lives = 3
        self.color = color
        self.direction = Direction.RIGHT
        self.KEYUP = shot
        

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

    def panel(self): #Уйдетсполя и не вернется
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

tank1 = Tank(100, 200, 2, (255, 0,0),pygame.K_RETURN)
tank2 = Tank(300 , 100 , 2 , (0,0,100),pygame.K_SPACE, pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)
tanks = [tank1,tank2]
class Bullet:
    def __init__(self, bullet_x = 0, bullet_y =0, bullet_color = (0, 0, 0), direction = 'RIGHT', bullet_speed = 11):
        self.bullet_x = bullet_x
        self.bullet_y = bullet_y
        self.bullet_speed = bullet_speed
        self.direction=direction
        self.bullet_color = bullet_color
        self.bullet_key = pygame.K_v



    def draw_bullet(self):
        pygame.draw.circle(screen, self.bullet_color, (self.bullet_x, self.bullet_y), 10)


    def move_bullet(self):

        if self.direction == Direction.UP:
            self.bullet_y -= self.bullet_speed

        if self.direction == Direction.DOWN:
            self.bullet_y += self.bullet_speed

        if self.direction == Direction.LEFT:
            self.bullet_x -= self.bullet_speed
            
        if self.direction == Direction.RIGHT:
            self.bullet_x += self.bullet_speed



        self.draw_bullet()


def shooting(tank):

    if tank.direction == Direction.UP:
        bullet_x = tank.x + tank.width // 2
        bullet_y = tank.y - tank.width // 2

    if tank.direction == Direction.DOWN:
        bullet_x = tank.x + tank.width // 2
        bullet_y = tank.y + tank.width + tank.width // 2

    if tank.direction == Direction.RIGHT:
        bullet_x = tank.x + tank.width + tank.width // 2
        bullet_y = tank.y + tank.width // 2

    if tank.direction == Direction.LEFT:
        bullet_x = tank.x - tank.width // 2
        bullet_y = tank.y + tank.width // 2

    

    b = Bullet(bullet_x, bullet_y, (0, 0, 0), tank.direction)
    bullets.append(b)

def HP1(x):
    font = pygame.font.SysFont("Arial",35)
    txt = font.render("Tank1:" + str(x),True,(0,0,0))
    screen.blit(txt,(20,20))

def HP2(x):
    font = pygame.font.SysFont("Arial",35)
    txt = font.render("Tank2:" + str(x),True,(0,0,0))
    screen.blit(txt,(520,20))
bullet1 = Bullet()
bullet2 = Bullet()
bullets = [bullet1, bullet2]



class Food:
    def __init__(self):
        self.x = random.randint(15,540)
        self.y = random.randint(15,540)


    def draw(self):
        screen.blit(foodImage,(self.x, self.y))
def encounter():
    if (food.x>= tank1.x and food.x <= tank1.x+135) and  (food.y >= tank1.y and food.y <= tank1.y+67):
        tank1.speed = 10
        # bullet1.speed = 100 
        food.x = random.randint(-100, -100)
        food.y = random.randint(-100, -100)
    if (food.x>= tank2.x and food.x <= tank2.x+135) and  (food.y >= tank2.y and food.y <= tank2.y+67):
        tank2.speed = 10
        # bullet_speed =  100
        
        food.x = random.randint(-100, -100)
        food.y = random.randint(-100,-100)

food = Food()

tank1 = Tank(100, 200, 2, (255, 0,0),pygame.K_RETURN)
tank2 = Tank(300 , 100 , 2 , (0,0,100),pygame.K_SPACE, 
pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)

bullet1 = Bullet()
bullet2 = Bullet()


tanks = [tank1, tank2]
bullets = [bullet1, bullet2]


def singleplayer_start():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((800,600))
    global width
    width = 800
    global height
    height = 600
    tank1 = Tank(100, 200, 2, (255, 0,0),pygame.K_RETURN)
    tank2 = Tank(300 , 100 , 2 , (0,0,100),pygame.K_SPACE, 
    pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)

    bullet1 = Bullet()
    bullet2 = Bullet()

    global tanks
    tanks = [tank1,tank2]
    global bullets
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
                        shooting(tank)
        screen.blit(backgroundimage, (0, 0))
        
    
        for tank in tanks:
            tank.move()
        
        
              
        for tank in tanks:
            tank.draw() 

        for tank in tanks:
            tank.panel()

        for b in bullets:
            b.move_bullet()
        
        HP1(tank1.lives)
        HP2(tank2.lives)
        # Encounter()
        # food.draw()
            
        for b in bullets:
            if b.bullet_x in range(tanks[0].x , tanks[0].x + 50) and b.bullet_y in range(tanks[0].y , tanks[0].y + 50): 
                tanks[0].lives -= 1
                bullets.remove(b)
                vzryv_sound.play()
            if b.bullet_x in range(tanks[1].x , tanks[1].x + 50) and b.bullet_y in range(tanks[1].y , tanks[1].y + 50): 
                tanks[1].lives -= 1
                bullets.remove(b)
                vzryv_sound.play()


            if tanks[0].lives == 0 or tanks[1].lives == 0:
                game = False
                font = pygame.font.SysFont('Impact', 80)
                word = font.render('Game Over', True, (0, 0, 0))
                coordinate = word.get_rect(center=(400, 275))
                screen.blit(word, coordinate)

                if tanks[0].lives == 0:
                    font1 = pygame.font.SysFont("Impact", 40)
                    word1 = font1.render('TANK2 Wins', True, (0, 0,100))
                    coordinate1 = word1.get_rect(center=(400, 500))
                    screen.blit(word1, coordinate1)

                if tanks[1].lives == 0:
                    font2 = pygame.font.SysFont("Impact", 40)
                    word2 = font2.render('TANK1 Wins', True, (255, 0, 0))
                    coordinate2 = word2.get_rect(center=(400, 500))
                    screen.blit(word2, coordinate2)
            
        # Encounter()
        food.draw()
              
        pygame.display.flip()

class TankRpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=IP,
        port = PORT,
        virtual_host = VHOST,
        credentials = pika.PlainCredentials(
            username = USER,
            password = PSSWRD
        )))
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue = '',
                                           auto_delete = True,
                                           exclusive = True)
        self.callback_queue = queue.method.queue #очередькудаприходит ответ
        self.channel.queue_bind(
            exchange = 'X:routing.topic',
            queue =  self.callback_queue
        )

        self.channel.basic_consume( 
            queue = self.callback_queue,
            on_message_callback = self.on_response,
            auto_ack = True
        )

        self.response = None
        self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None
    def on_response(self, ch, method, props, body):#принимает данные
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            print(self.response)


    def call(self, key, message = {}): #отправляет запросы на сервер

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body = json.dumps(message)
        )
        while self.response is None:
            self.connection.process_data_events()
        
    def check_server_status(self): #запрос чтобы узнатьстатус сервера
        self.call('tank.request.healthcheck')
        return self.response['status'] == '200'

    def obtain_token(self, room_id): 
        message = {
            'roomId': room_id
        }
        self.call('tank.request.register',message)
        if 'token' in  self.response:
            self.token = self.response['token']
            self.tank_id = self.response['tankId']
            self.room_id = self.response['roomId']
            return True
        return False

    def turn_tank(self, token,direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)

    def fire_bullet(self,token):
        message = {
            'token': token
        }
        self.call('tank.request.fire', message)

class TankConsumerClient(Thread):
    def __init__(self,room_id):
        super().__init__()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,
                port = PORT,
                virtual_host = VHOST,
                credentials = pika.PlainCredentials(
                    username = USER,
                    password = PSSWRD
        )))
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue = '',
                                           auto_delete = True,
                                           exclusive = True)
        event_listener = queue.method.queue
        self.channel.queue_bind(exchange = 'X:routing.topic',
                                queue = event_listener,
                                routing_key = 'event.state.'+ room_id)
        self.channel.basic_consume(
            queue = event_listener,
            on_message_callback= self.on_response,
            auto_ack = True
        )
        self.response = None
    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)

    def run(self):
        self.channel.start_consuming()
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

MOVE_KEYS = {
    pygame.K_w:UP,
    pygame.K_a:LEFT,
    pygame.K_s:DOWN,
    pygame.K_d:RIGHT
}

def get_tank_color(id):
    if id == client.tank_id:
        return (255, 0, 0)
    id = int(id[5:])
    return (0, 35 * id % 256, 16 * id % 256)

def get_bullet_color(id):
    return tuple(x // 3 for x in get_tank_color(id))

def draw_tank(**kwargs):
    tank_color = get_tank_color(kwargs['id'])
    tank_c = (kwargs['x'] + int(kwargs['width'] / 2), kwargs['y'] + int(kwargs['width'] / 2))
    pygame.draw.rect(screen, tank_color,
                    (kwargs['x'], kwargs['y'], kwargs['width'], kwargs['width']), 2)
    pygame.draw.circle(screen, tank_color, tank_c, int(kwargs['width'] / 2))


def draw_bullet(**kwargs):
    bullet_color = get_bullet_color(kwargs['owner'])
    pygame.draw.rect(screen, bullet_color, (kwargs['x'], kwargs['y'],kwargs['width'],kwargs['height']), 10)


class Leaderboard:
    def __init__(self, x, y, width, height,func):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.func = func
    def draw(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('HELLO', True, (255,255, 0))
        textRect = text.get_rect()
        textRect.center = (self.x, self.y)
        screen.blit(text, textRect)
    def draw_score(self, tanks):
        tanks_dict = {}
        offset = 0
        header_string = '{tank_id_header:<15s}{score_header:<9s}{health_header:<9s}'.format(
                tank_id_header = 'Tank ID',
                score_header = 'Score',
                health_header = 'Health')
        font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render(header_string, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.topleft = (self.x, self.y + offset)
        screen.blit(text, textRect)
        offset += 15

        for tank in tanks:
            tanks_dict[tank['id']] = tank
            print(tanks_dict)
        for tank in sorted(tanks_dict.values(), key = lambda item: item['score'], reverse = True):
            tank_table_string = '{tank_id:<15s}{score:<12s}{health:<9s}'.format(
                    tank_id = tank['id'],
                    score = str(tank['score']),
                    health = str(tank['health']))
            font = pygame.font.Font('freesansbold.ttf', 15)
            text = font.render(tank_table_string, True, get_tank_color(tank['id']))
            textRect = text.get_rect()
            textRect.topleft = (self.x, self.y + offset)
            screen.blit(text, textRect)
            offset += 15



def click_button():
    print('OK')

class GameOverStatus(Enum):
    NONE = 0
    WIN = 1
    LOSS = 2
    KICK = 3

def find_self_in(winners, losers, kicked):
    for winner in winners:
        if winner['tankId'] == client.tank_id:
            return GameOverStatus.WIN
            # print(winner)
    for loser in losers:
        if loser['tankId'] == client.tank_id:
            return GameOverStatus.LOSS
    for tank in kicked:
        if tank['tankId'] == client.tank_id:
            return GameOverStatus.KICK
    return GameOverStatus.NONE

def draw_game_over_text(game_over_reason):
    game_over_text = 'INTERNAL ERROR'
    if game_over_reason == GameOverStatus.WIN:
        game_over_text = 'YOU WON!'
    elif game_over_reason == GameOverStatus.LOSS:
        game_over_text = 'YOU LOST!'
    elif game_over_reason == GameOverStatus.KICK:
        game_over_text = 'YOU WERE KICKED!'
    game_over_subtext = 'Press \'R\' to restart the game.'

    font = pygame.font.Font('freesansbold.ttf', 42)
    text = font.render(game_over_text, True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.center = (400, 300)
    screen.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 24)
    text = font.render(game_over_subtext, True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.center = (400, 400)
    screen.blit(text, textRect)

def multiplayer_start():
    global client
    client = TankRpcClient()
    client.check_server_status()
    client.obtain_token(ROOM)
    global event_client
    event_client = TankConsumerClient(ROOM)
    event_client.start()

    mainloop = True
    game_over = False
    game_over_reason = GameOverStatus.NONE
    font = pygame.font.Font('freesansbold.ttf', 28)
    leaderboard = Leaderboard(10, 10, 100, 100, click_button)
    while mainloop:
        screen.fill((0, 0, 0))

        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                mainloop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                if event.key in MOVE_KEYS:
                    client.turn_tank(client.token, MOVE_KEYS[event.key])
                if event.key == pygame.K_SPACE:
                    client.fire_bullet(client.token)
                if event.key == pygame.K_r and game_over:
                    game_over = False
                    game_over_reason = GameOverStatus.NONE
                    client = TankRpcClient()
                    client.check_server_status()
                    client.obtain_token(ROOM)
                    event_client = TankConsumerClient(ROOM)
                    event_client.start()

        try:
            remaining_time = event_client.response['remainingTime']
            text = font.render('Remaining Time:{}'.format(remaining_time), True, (255,255,255))
            textRect = text.get_rect()
            textRect.center = (630, 20)
            screen.blit(text, textRect)
            hits = event_client.response['hits']
            
            bullets = event_client.response['gameField']['bullets']
            # print(bullets)
            # print(gameField)
            winners = event_client.response['winners']
            losers = event_client.response['losers']
            kicked = event_client.response['kicked']
            tanks = event_client.response['gameField']['tanks']
            for tank in tanks:
                draw_tank(**tank)
            for bullet in bullets:
                draw_bullet(**bullet)
            leaderboard.draw_score(tanks)
            game_over_status = find_self_in(winners, losers, kicked)
            if game_over_status != GameOverStatus.NONE:
                game_over = True
                game_over_reason = game_over_status

            if game_over:
                draw_game_over_text(game_over_reason)

        except:
            pass
        pygame.display.flip()

    client.connection.close()
class Button:
    def __init__(self, x, y, width, height, color, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text

    def draw(self):
        font_color = (0, 0 ,0 )
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render(self.text, True, font_color)
        textRect = text.get_rect()
        textRect.topleft = (self.x, self.y)
        textRect.size = (self.width, self.height)
        pygame.draw.rect(screen, self.color, textRect)
        screen.blit(text, textRect)

    def is_in(self, x, y):
        if x > self.x and \
                x < self.x + self.width and \
                y > self.y and \
                y < self.y + self.height:
            return True
        return False

def start_menu():
    singleplayer_button = Button(100, 100, 500, 100, (0, 255, 0), 'Single Player')
    multiplayer_button = Button(100, 300, 500, 100, (255, 0, 0), 'Multi Player')
    aiplayer_button = Button(100, 500,500, 100,(255,255,0),'AI Player')
    mainloop = True
    while mainloop:
        screen.fill((255,255,255))
        singleplayer_button.draw()
        multiplayer_button.draw()
        aiplayer_button.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if singleplayer_button.is_in(event.pos[0], event.pos[1]):
                        singleplayer_start()
                        pygame.quit()
                        sys.exit(0)
                    if multiplayer_button.is_in(event.pos[0], event.pos[1]):
                        multiplayer_start()
                        pygame.quit()
                        sys.exit(0)
        pygame.display.flip()

start_menu() 
encounter()
pygame.init()
pygame.mixer.init()
