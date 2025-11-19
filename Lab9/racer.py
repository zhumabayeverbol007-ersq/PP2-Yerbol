import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
clock = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

W, H = 400, 600
vel = 5
score = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

game_over = font.render("Game Over", True, BLACK)

bg = pygame.image.load(r"C:\Users\LENOVO\OneDrive\Документы\GitHub\PP2-Yerbol\PP2\Lab8\materials\AnimatedStreet.png")   # 🔥 Фон суретінің жолы

win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Racer ╚(•⌂•)╝")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\LENOVO\OneDrive\Документы\GitHub\PP2-Yerbol\PP2\Lab8\materials\Enemy.png")  # 🔥 Enemy суреті
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, W - 40), 0)

    def move(self):
        global score, vel
        self.rect.move_ip(0, vel)
        if self.rect.top > H:
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, W - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        coin_paths = [
            r"C:\Users\LENOVO\OneDrive\Документы\GitHub\PP2-Yerbol\PP2\Lab9\new_materials\coin1.png",
            r"C:\Users\LENOVO\OneDrive\Документы\GitHub\PP2-Yerbol\PP2\Lab9\new_materials\coin2.png",
            r"C:\Users\LENOVO\OneDrive\Документы\GitHub\PP2-Yerbol\PP2\Lab9\new_materials\Coin3.png"
        ]

        self.type = random.randint(0, 2)
        self.image = pygame.image.load(coin_paths[self.type])
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, W - 40), 0)
        self.weights = [1, 2, 3]
        self.value = self.weights[self.type]

    def move(self):
        self.rect.move_ip(0, vel)
        if self.rect.top > H:
            self.rect.top = 0
            self.rect.center = (random.randint(40, W - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\LENOVO\OneDrive\Документы\GitHub\PP2-Yerbol\PP2\Lab8\materials\Player.png")  # 🔥 Player.png
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < W:
            if pressed[K_RIGHT]:
                self.rect.move_ip(5, 0)


P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

coin_cnt = 0

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            vel += 0.2
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    win.blit(bg, (0, 0))

    scores = font_small.render("Score: " + str(score), True, BLACK)
    coin_text = font_small.render("Coins: " + str(coin_cnt), True, BLACK)

    win.blit(scores, (10, 10))
    win.blit(coin_text, (300, 10))

    for entity in all_sprites:
        win.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound(r"C:\Users\LENOVO\OneDrive\Документы\GitHub\PP2-Yerbol\PP2\Lab8\materials\crash.wav").play()  # 🔥 crash.wav
        time.sleep(0.5)
        win.fill(RED)
        win.blit(game_over, (30, 250))
        pygame.display.update()

        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    collided_coins = pygame.sprite.spritecollide(P1, coins, True)

    for coin in collided_coins:
        coin_cnt += coin.value

        if coin_cnt % 10 == 0:
            vel += 1

    if len(coins) < 1:
        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)

    pygame.display.update()
    clock.tick(FPS)