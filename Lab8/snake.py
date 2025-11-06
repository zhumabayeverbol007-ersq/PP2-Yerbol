import pygame, random, time
pygame.init()

W, H = 620, 400
S = 20
BASE_SPEED = 10

LIGHT_GREEN = (175, 215, 70)
GREEN = (167, 209, 61)
PURPLE = (63, 104, 224)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake Game")
font = pygame.font.Font(None, 30)

def text(txt, x, y, color=(0,0,0)):
    surf = font.render(txt, True, color)
    win.blit(surf, (x, y))
#d=DRAW
def d_snake(body):
    for x, y in body:
        pygame.draw.rect(win, PURPLE, (x, y, S, S))

def d_food(pos):
    pygame.draw.rect(win, RED, (pos[0], pos[1], S, S))

def d_bg():
    for y in range(0, H, S):
        for x in range(0, W, S):
            color = LIGHT_GREEN if (x//S + y//S) % 2 == 0 else GREEN
            pygame.draw.rect(win, color, (x, y, S, S))

def new_food(snake):
    while True:
        fx = random.randint(0, (W - S) // S) * S
        fy = random.randint(0, (H - S) // S) * S
        if (fx, fy) not in snake:
            return (fx, fy)

def play():
    snake = [(100, 100), (80, 100), (60, 100)]
    dir = "RIGHT"
    food = new_food(snake)
    score = 0
    lvl = 1
    speed = BASE_SPEED
    clock = pygame.time.Clock()
    run = True

    while run:
        d_bg()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                pygame.quit()
                return
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and dir != "DOWN":
                    dir = "UP"
                elif e.key == pygame.K_DOWN and dir != "UP":
                    dir = "DOWN"
                elif e.key == pygame.K_LEFT and dir != "RIGHT":
                    dir = "LEFT"
                elif e.key == pygame.K_RIGHT and dir != "LEFT":
                    dir = "RIGHT"

        hx, hy = snake[0]
        if dir == "UP":
            hy -= S
        elif dir == "DOWN":
            hy += S
        elif dir == "LEFT":
            hx -= S
        elif dir == "RIGHT":
            hx += S

        head = (hx, hy)
        if hx < 0 or hx >= W or hy < 0 or hy >= H or head in snake:
            d_bg()
            text("Game Over!", W//2 - 70, H//2 - 20, RED)
            text(f"Your score: {score}", W//2 - 80, H//2 + 10)
            pygame.display.update()
            time.sleep(2)
            return

        snake.insert(0, head)

        if head == food:
            score += 1
            food = new_food(snake)
            if score % 3 == 0:
                lvl += 1
                speed += 2
        else:
            snake.pop()

        d_snake(snake)
        d_food(food)
        text(f"Score: {score}", 10, 10)
        text(f"Level: {lvl}", 500, 10)

        pygame.display.update()
        clock.tick(speed)
play()
