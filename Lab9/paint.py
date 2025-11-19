import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Paint (◕‿◕)")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

font = pygame.font.Font(None, 28)

radius = 15
mode = "qalam"
color = GREEN
drawing = False
start_pos = None
points = []

buttons = {
    "qalam": pygame.Rect(10, 10, 100, 30),
    "rect": pygame.Rect(120, 10, 130, 30),
    "circle": pygame.Rect(260, 10, 130, 30),
    "eraser": pygame.Rect(400, 10, 100, 30),
    "square": pygame.Rect(10, 50, 100, 30),
    "rtriangle": pygame.Rect(120, 50, 130, 30),
    "etriangle": pygame.Rect(260, 50, 130, 30),
    "rhombus": pygame.Rect(400, 50, 100, 30),
}
color_buttons = {
    "red": pygame.Rect(530, 10, 30, 30),
    "green": pygame.Rect(570, 10, 30, 30),
    "blue": pygame.Rect(610, 10, 30, 30),
    "yellow": pygame.Rect(650, 10, 30, 30),
}

def d_ui():
    pygame.draw.rect(screen, GRAY, (0, 0, 800, 90))
    for name, rect in buttons.items():
        pygame.draw.rect(screen, CYAN if mode == name else WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        
        display_names = {
            "qalam": "Qalam",
            "rect": "rect",
            "circle": "circle",
            "eraser": "eraser",
            "square": "Sharshy",
            "rtriangle": "rtriangle",
            "etriangle": "etriangle",
            "rhombus": "Romb"
        }
        
        text = font.render(display_names[name], True, BLACK)
        screen.blit(text, (rect.x + 5, rect.y + 5))
    
    for cname, rect in color_buttons.items():
        cval = eval(cname.upper())
        pygame.draw.rect(screen, cval, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        if color == cval:
            pygame.draw.rect(screen, (255, 255, 0), rect, 3)

def dLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))
    if color_mode == RED:
        color = (c2, c1 // 2, c1 // 2)
    elif color_mode == GREEN:
        color = (c1 // 2, c2, c1 // 2)
    elif color_mode == BLUE:
        color = (c1 // 2, c1 // 2, c2)
    elif color_mode == YELLOW:
        color = (c2, c2, c1 // 2)
    else:
        color = color_mode
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    for i in range(iterations):
        progress = i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

def draw_square(start, end, color, width=3):
    side = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
    x1, y1 = start
    x2 = x1 + side if end[0] > start[0] else x1 - side
    y2 = y1 + side if end[1] > start[1] else y1 - side
    
    points = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    pygame.draw.polygon(screen, color, points, width)

def draw_right_triangle(start, end, color, width=3):
    x1, y1 = start
    x2, y2 = end

    points = [(x1, y1), (x2, y1), (x1, y2)]
    pygame.draw.polygon(screen, color, points, width)

def draw_equilateral_triangle(start, end, color, width=3):
    x1, y1 = start
    x2, y2 = end
    
    base = abs(x2 - x1)
    height = base * math.sqrt(3) / 2
    
    if y2 > y1:
        points = [
            (x1, y1),
            (x2, y1),
            ((x1 + x2) // 2, y1 + height)
        ]
    else:
        points = [
            (x1, y1),
            (x2, y1),
            ((x1 + x2) // 2, y1 - height)
        ]
    
    pygame.draw.polygon(screen, color, points, width)

def draw_rhombus(start, end, color, width=3):
    x1, y1 = start
    x2, y2 = end
    
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    width_half = abs(x2 - x1) // 2
    height_half = abs(y2 - y1) // 2
    
    points = [
        (center_x, y1),
        (x2, center_y),
        (center_x, y2),
        (x1, center_y)
    ]
    
    pygame.draw.polygon(screen, color, points, width)

screen.fill(BLACK)
running = True
while running:
    pressed = pygame.key.get_pressed()
    ctrl = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
    alt = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]

    if pressed[pygame.K_ESCAPE] or (pressed[pygame.K_w] and ctrl) or (pressed[pygame.K_F4] and alt):
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if pos[1] <= 90:
                for name, rect in buttons.items():
                    if rect.collidepoint(pos):
                        mode = name
                        points.clear()
                        start_pos = None
                for cname, rect in color_buttons.items():
                    if rect.collidepoint(pos):
                        color = eval(cname.upper())
            else:
                drawing = True
                start_pos = pos
                if mode == "qalam":
                    points.append(pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos:
                end = event.pos
                if mode == "rect":
                    pygame.draw.rect(screen, color, pygame.Rect(start_pos, (end[0] - start_pos[0], end[1] - start_pos[1])), 4)
                elif mode == "circle":
                    r = int(((end[0] - start_pos[0]) ** 2 + (end[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, r, 3)
                elif mode == "square":
                    draw_square(start_pos, end, color, 4)
                elif mode == "rtriangle":
                    draw_right_triangle(start_pos, end, color, 4)
                elif mode == "etriangle":
                    draw_equilateral_triangle(start_pos, end, color, 4)
                elif mode == "rhombus":
                    draw_rhombus(start_pos, end, color, 4)
            drawing = False
            start_pos = None
            points.clear()

        elif event.type == pygame.MOUSEMOTION and drawing:
            if mode == "qalam":
                pos = event.pos
                points.append(pos)
                points = points[-256:]
            elif mode == "eraser":
                pygame.draw.circle(screen, BLACK, event.pos, 80)

    if mode == "qalam" and len(points) > 1:
        for i in range(len(points) - 1):
            dLineBetween(screen, i, points[i], points[i + 1], radius, color)

    d_ui()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()