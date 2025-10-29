import pygame
import datetime

pygame.init()

WIDTH = 1400
HEIGHT = 1050

FPS = 60

time = datetime.datetime.now()
angle = -(int(time.strftime("%S")) * 6) - 6
angleM = -(int(time.strftime("%M")) * 6 + (int(time.strftime("%S")) * 6 / 60)) - 54

background = pygame.image.load(r'C:\Users\LENOVO\OneDrive\Документы\GitHub\PP2-Yerbol\PP2\Lab7\Clock.png')
second = pygame.image.load(r'C:\Users\LENOVO\OneDrive\Документы\GitHub\PP2-Yerbol\PP2\Lab7\second.png')
minute = pygame.image.load(r'C:\Users\LENOVO\OneDrive\Документы\GitHub\PP2-Yerbol\PP2\Lab7\minute.png')


def rotate(image, rect, angle):
    new_image = pygame.transform.rotate(image, angle)
    rect = new_image.get_rect(center = rect.center)
    return new_image, rect


# second
image = pygame.Surface((63, HEIGHT), pygame.SRCALPHA)
image.blit(second, (0, 0))
orig_image = image
rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# minute
imagem = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
imagem.blit(minute, (0, 0))
orig_imagem = imagem
rect1 = imagem.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    screen.blit(image, rect)
    screen.blit(imagem, rect1)
    image, rect = rotate(orig_image, rect, angle)
    imagem, rect1 = rotate(orig_imagem, rect1, angleM)

    angle -= 0.099
    angleM -= 0.099 / 60

    pygame.display.flip()

pygame.quit()