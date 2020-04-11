import pygame
import random
from time import sleep
pygame.init()
pygame.font.init()

# Настраиваем экран
size = width, height = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Basic Arcanoid (Premitive physics)')

# Настраиваем переменные
IsStart = 0
Lives = 3
Score = 0
Combo = 1
clock = pygame.time.Clock()
fps = 30

# Заносим звуки в переменные
BounceSNew = pygame.mixer.Sound('data/Sounds/BlockHit.ogg')
BouncePlayerS = pygame.mixer.Sound('data/Sounds/ArcPlateHit.ogg')
BrickDestroyS = pygame.mixer.Sound('data/Sounds/BlockHitBreaking.ogg')

# Создаём удобную функцию загрузки спрайтов
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

# Создаём класс платформы
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

# Создаём класс кирпичика
class Brick(pygame.sprite.Sprite):

    image = load_image('Bricks/Gray.png')
    Red = load_image('Bricks/Red.png')
    Green = load_image('Bricks/Green.png')
    Blue = load_image('Bricks/Blue.png')
    Orange = load_image('Bricks/Orange.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(Bricks)
        self.image = Brick.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.colorv = random.randint(1, 9) # 1 - 5 - Gray, 6 - Green, 7 - Blue, 8 - Red, 9 - Orange. Случайно выбираем цвет кирпичика

        if self.colorv >= 1 and self.colorv <= 5:
            self.image = Brick.image
        elif self.colorv == 6:
            self.image = Brick.Green
        elif self.colorv == 7:
            self.image = Brick.Blue
        elif self.colorv == 8:
            self.image = Brick.Red
        elif self.colorv == 9:
            self.image = Brick.Orange

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)

        # При соприкосновении мячика с кирпичиком
        if pygame.sprite.spritecollide(self, BallG, False):
            global Combo
            global Score

            Score += 5 * Combo
            Combo += 1
            BounceSNew.play()

            if self.image == Brick.image:
                BrickBlow(self.rect.x, self.rect.y)
                BrickDestroyS.play()
                self.kill()
            else:
                self.image = Brick.image

# Создаём класс мячика
class Ball(pygame.sprite.Sprite):

    image = load_image('Ball.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(BallG) # Добавляем мяч в специальную группу для взаимодействий
        self.image = pygame.transform.scale(Ball.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.rdirb = 0
        self.rdirp = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy) # Двигаем мячик

        # При соприкосновении с кирпичиком меняем направление и проигрываем звук
        if pygame.sprite.spritecollide(self, Bricks, False):

            BounceSNew.play()

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

        # Отскакиваем от платформы
        if pygame.sprite.spritecollide(self, P1, False):
            global Combo
            BouncePlayerS.play()
            Combo = 1
            self.rdirp = random.randint(1, 2)

            if self.rdirp == 1:
                self.vx = self.vx
                self.vy = -self.vy
            elif self.rdirp == 2:
                self.vx = -self.vx
                self.vy = -self.vy

        # Отскакиваем от границ экрана
        if self.rect.y <= 0:
            self.vx = self.vx
            self.vy = -self.vy

        if self.rect.x >= 1250 or self.rect.x <= 0:
            self.vx = -self.vx
            self.vy = self.vy

        # Мячик улител за платформу, теряем одну жизнь
        if self.rect.y >= 720:
            self.foul()

    # Функция старта мячика
    def go(self):
        global IsStart
        self.vx = -4
        self.vy = -4
        IsStart = 1

    # Функция для потери жизни
    def foul(self):
        global IsStart
        global Lives
        global Combo
        if Lives > 0:
            self.vx = 0
            self.vy = 0
            self.rect.x = 628
            self.rect.y = 550
            Player.rect.x = 540
            IsStart = 0
            Lives -= 1
            Combo = 1
        elif Lives <= 0:
            self.vx = 0
            self.vy = 0
            self.rect.x = -100
            self.rect.y = -100
            IsStart = 2
            Combo = 1

# Создаём класс под задний фон
class Background(pygame.sprite.Sprite):

    image = load_image('ArcBG.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Background.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Создаём класс под анимацию уничтожения кирпичика
class BrickBlow(pygame.sprite.Sprite):

    image = load_image('BrickBreaking/BlockBrake1.png')

    images = ['BrickBreaking/BlockBrake1.png', 'BrickBreaking/BlockBrake2.png', 'BrickBreaking/BlockBrake3.png',
              'BrickBreaking/BlockBrake4.png', 'BrickBreaking/BlockBrake5.png', 'BrickBreaking/BlockBrake6.png',
              'BrickBreaking/BlockBrake7.png', 'BrickBreaking/BlockBrake8.png', 'BrickBreaking/BlockBrake9.png',
              'BrickBreaking/BlockBrake10.png', 'BrickBreaking/BlockBrake11.png', 'BrickBreaking/BlockBrake12.png',
              'BrickBreaking/BlockBrake13.png', 'BrickBreaking/BlockBrake14.png', 'BrickBreaking/BlockBrake15.png',
              'BrickBreaking/BlockBrake16.png', 'BrickBreaking/BlockBrake17.png', 'BrickBreaking/BlockBrake18.png'
              ]

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = BrickBlow.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animtimer = 1
        self.frame = 0

    def update(self):

        self.preload_image = load_image(BrickBlow.images[self.frame])
        self.image = self.preload_image

        if self.frame < 17:
            self.frame += 1

        if self.frame == 17:
            self.kill()

# Задаём шрифт игры и так-же создаём тексты
GameFont = pygame.font.SysFont('calibri', 30)
ScoreText = GameFont.render('Score: ' + str(Score), 1, (255, 255, 255))
ComboText = GameFont.render('Combo: ' + str(Combo), 1, (255, 255, 255))
LivesText = GameFont.render('Lives: ' + str(Lives), 1, (255, 255, 255))

# Создаём группы взаимодействий
all_sprites = pygame.sprite.Group()
P1 = pygame.sprite.Group()
BallG = pygame.sprite.Group()
Bricks = pygame.sprite.Group()

# Создаём объекты
BackGroundObj = Background(0, 0)
Player = Paddle(540, 640)
PBall = Ball(628, 550)

# Создаём кирпичики
brk_x, brk_y = 50, 100
for i in range(7):
    for j in range(9):
        Brick(brk_x, brk_y)

        brk_x += 128
    brk_y += 32
    brk_x -= 9 * 128

# Главный цикл игры
running = True
while running:

    # Управление персонажем
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and IsStart == 1 and Player.rect.x < 1080:
        Player.rect.x += 6
    if keys[pygame.K_LEFT] and IsStart == 1 and Player.rect.x > 0:
        Player.rect.x -= 6

    # Проверка на уничтожение всех кирпичиков
    if len(Bricks) <= 0:
        PBall.vx = 0
        PBall.vy = 0
        IsStart = 3

    # При нажатии Space вызываем функцию старта у мячика
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and IsStart == 0 and Lives > 0:
            IsStart == 1
            PBall.go()


        if event.type == pygame.QUIT:
            running = False

    # Рендерим (рисуем) все объекты на экран
    screen.fill((0, 0, 0))

    ScoreText = GameFont.render('Score: ' + str(Score), 1, (255, 255, 255))
    ComboText = GameFont.render('Combo: ' + str(Combo), 1, (255, 255, 255))

    if Lives > 0 :
        LivesText = GameFont.render('Lives: ' + str(Lives), 1, (255, 255, 255))
    elif Lives <= 0:
        LivesText = GameFont.render('Game Over!', 1, (255, 255, 255))
    elif Lives > 0 and IsStart == 3:
        LivesText = GameFont.render('You Win!', 1, (255, 255, 255))

    for sprite in all_sprites:
        sprite.update()
    all_sprites.draw(screen)
    screen.blit(ScoreText, (20, 20))
    screen.blit(ComboText, (20, 660))
    screen.blit(LivesText, (20, 630))
    pygame.display.flip()
    pygame.time.delay(20)
    clock.tick(fps)