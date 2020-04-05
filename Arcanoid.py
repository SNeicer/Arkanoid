import pygame
import random
from time import sleep
pygame.init()
pygame.font.init()


size = width, height = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Basic Arcanoid (Premitive physics)')
IsStart = 0
Lives = 3
Score = 0
Combo = 1
clock = pygame.time.Clock()
fps = 45

BounceS = pygame.mixer.Sound('data/Sounds/Bounce.wav')
GoalS = pygame.mixer.Sound('data/Sounds/Goal.wav')
LoseS = pygame.mixer.Sound('data/Sounds/Lose.wav')

def load_image(name):
    fullname = 'data' + '/' + name
    try:
        if name[-2:] == 'jpg':
            image = pygame.image.load(fullname).convert()
        else:
            image = pygame.image.load(fullname).convert_alpha()
    except:
        print('Cannot load image: ', name)
        raise SystemExit()

    return image

class Paddle(pygame.sprite.Sprite):

    image = load_image('Paddle.png')
    
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(P1)
        self.image = Paddle.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)

class Brick(pygame.sprite.Sprite):

    image = load_image('Brick.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(Bricks)
        self.image = Brick.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)

class Ball(pygame.sprite.Sprite):

    image = load_image('Ball.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(Ball.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.rdirb = 0
        self.rdirp = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)

        if pygame.sprite.spritecollide(self, Bricks, True):
            global Combo
            global Score
            Score += 5 * Combo
            Combo += 1
            BounceS.play()


            self.rdirb = random.randint(1, 3)
            if self.rdirb == 1:
                self.vx = self.vx
                self.vy = -self.vy
            elif self.rdirb == 2:
                self.vx = -self.vx
                self.vy = -self.vy
            elif self.rdirb == 3:
                self.vx = -self.vx
                self.vy = self.vy

        if pygame.sprite.spritecollide(self, P1, False):
            BounceS.play()
            Combo = 1
            self.rdirp = random.randint(1, 2)

            if self.rdirp == 1:
                self.vx = self.vx
                self.vy = -self.vy
            elif self.rdirp == 2:
                self.vx = -self.vx
                self.vy = -self.vy

        if self.rect.y <= 0:
            self.vx = self.vx
            self.vy = -self.vy

        if self.rect.x >= 1250 or self.rect.x <= 0:
            self.vx = -self.vx
            self.vy = self.vy

        if self.rect.y >= 720:
            self.foul()


    def go(self):
        global IsStart
        self.vx = -4
        self.vy = -4
        IsStart = 1

    def foul(self):
        global IsStart
        global Lives
        global Combo
        if Lives > 0:
            self.vx = 0
            self.vy = 0
            self.rect.x = 640
            self.rect.y = 550
            Player.rect.x = 580
            IsStart = 0
            Lives -= 1
            Combo = 1
            LoseS.play()
        elif Lives <= 0:
            self.vx = 0
            self.vy = 0
            self.rect.x = -100
            self.rect.y = -100
            IsStart = 2
            Combo = 1

GameFont = pygame.font.SysFont('calibri', 30)
ScoreText = GameFont.render('Score: ' + str(Score), 1, (255, 255, 255))
ComboText = GameFont.render('Combo: ' + str(Combo), 1, (255, 255, 255))
LivesText = GameFont.render('Lives: ' + str(Lives), 1, (255, 255, 255))


all_sprites = pygame.sprite.Group()
P1 = pygame.sprite.Group()
Bricks = pygame.sprite.Group()

Player = Paddle(580, 640)
PBall = Ball(640, 550)


brk_x, brk_y = 40, 100
for i in range(5):
    for j in range(10):
        Brick(brk_x, brk_y)

        brk_x += 120
    brk_y += 50
    brk_x -= 10 * 120

running = True
while running:

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and IsStart == 1:
        Player.rect.x += 6
    if keys[pygame.K_LEFT] and IsStart == 1:
        Player.rect.x -= 6

    if len(Bricks) <= 0:
        GoalS.play()
        PBall.vx = 0
        PBall.vy = 0
        IsStart = 3


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and IsStart == 0 and Lives > 0:
            IsStart == 1
            PBall.go()


        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    ScoreText = GameFont.render('Score: ' + str(Score), 1, (255, 255, 255))
    ComboText = GameFont.render('Combo: ' + str(Combo), 1, (255, 255, 255))

    if Lives > 0 :
        LivesText = GameFont.render('Lives: ' + str(Lives), 1, (255, 255, 255))
    elif Lives <= 0:
        LivesText = GameFont.render('Game Over!', 1, (255, 255, 255))
    elif Lives > 0 and IsStart == 3:
        LivesText = GameFont.render('You Win!', 1, (255, 255, 255))

    screen.blit(ScoreText, (20, 20))
    screen.blit(ComboText, (20, 660))
    screen.blit(LivesText, (20, 630))

    for sprite in all_sprites:
        sprite.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    pygame.time.delay(20)
    clock.tick(fps)