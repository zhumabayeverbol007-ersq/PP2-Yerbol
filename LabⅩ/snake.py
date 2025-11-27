import pygame, random, time, psycopg2
pygame.init()

W, H = 620, 400
S = 20
BASE_SPEED = 10
COLORS = {
    "LIGHT_GREEN": (175, 215, 70),
    "GREEN": (167, 209, 61),
    "PURPLE": (63, 104, 224),
    "RED": (255, 0, 0),
    "ORANGE": (255, 165, 0),
    "YELLOW": (255, 255, 0),
    "BLACK": (0, 0, 0),
    "GRAY": (100, 100, 100)
}

win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake Game")
font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 24)

DB = {
    'dbname':'snake',
    'user':'postgres',
    'password':'1234',
    'host':'localhost',
    'port':'5433'
}

def setup_db():
    conn = psycopg2.connect(**DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_scores(
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            score INTEGER,
            level INTEGER,
            snake_body TEXT,
            direction VARCHAR(10),
            food_pos TEXT,
            food_weight INTEGER,
            food_lifetime REAL,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_conn():
    return psycopg2.connect(**DB)

def get_user_id(username):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=%s", (username,))
    res = c.fetchone()
    if res:
        user_id = res[0]
    else:
        c.execute("INSERT INTO users(username) VALUES(%s) RETURNING id", (username,))
        user_id = c.fetchone()[0]
        conn.commit()
    conn.close()
    return user_id

def save_state(user_id, score, level, snake, direction, food):
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        INSERT INTO user_scores(user_id, score, level, snake_body, direction, food_pos, food_weight, food_lifetime)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    ''', (user_id, score, level, str(snake), direction, str(food["pos"]), food["weight"], food["lifetime"]))
    conn.commit()
    conn.close()

def load_state(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        SELECT score, level, snake_body, direction, food_pos, food_weight, food_lifetime
        FROM user_scores
        WHERE user_id=%s
        ORDER BY saved_at DESC
        LIMIT 1
    ''', (user_id,))
    res = c.fetchone()
    conn.close()
    return res

def draw_text(txt, x, y, color=COLORS["BLACK"], font_type=font):
    win.blit(font_type.render(txt, True, color), (x, y))

def draw_bg(level=1):
    for y in range(0,H,S):
        for x in range(0,W,S):
            c = COLORS["LIGHT_GREEN"] if (x//S + y//S)%2==0 else COLORS["GREEN"]
            pygame.draw.rect(win, c, (x,y,S,S))
    if level==2:
        for x in range(0,W,S):
            pygame.draw.rect(win, COLORS["GRAY"], (x,0,S,S))
            pygame.draw.rect(win, COLORS["GRAY"], (x,H-S,S,S))
        for y in range(0,H,S):
            pygame.draw.rect(win, COLORS["GRAY"], (0,y,S,S))
            pygame.draw.rect(win, COLORS["GRAY"], (W-S,y,S,S))
    elif level==3:
        mx, my = W//2, H//2
        for i in range(-2,3):
            pygame.draw.rect(win,COLORS["GRAY"],(mx+i*S,my-2*S,S,S))
            pygame.draw.rect(win,COLORS["GRAY"],(mx,my+i*S,S,S))
    elif level>=4:
        for x in range(3*S,8*S,S):
            pygame.draw.rect(win,COLORS["GRAY"],(x,3*S,S,S))
            pygame.draw.rect(win,COLORS["GRAY"],(x,H-4*S,S,S))
        for y in range(5*S,10*S,S):
            pygame.draw.rect(win,COLORS["GRAY"],(W-5*S,y,S,S))

def draw_snake(body):
    for x,y in body:
        pygame.draw.rect(win,COLORS["PURPLE"],(x,y,S,S))

def draw_food(food):
    colors = [COLORS["RED"], COLORS["ORANGE"], COLORS["YELLOW"]]
    pygame.draw.rect(win, colors[food["weight"]-1], (*food["pos"], S, S))
    win.blit(font.render(str(food["weight"]), True, COLORS["LIGHT_GREEN"]),
             (food["pos"][0]+5, food["pos"][1]+2))

def new_food(snake, level=1):
    while True:
        fx = random.randint(0,(W-S)//S)*S
        fy = random.randint(0,(H-S)//S)*S
        if (fx,fy) not in snake and not is_wall((fx,fy), level):
            return {"pos":(fx,fy), "weight":random.randint(1,3), "lifetime":time.time()+random.randint(5,8)}

def is_wall(pos, level):
    x, y = pos
    S_range = lambda val, center, n: center - n*S <= val <= center + n*S
    if level == 2:
        return x == 0 or x == W-S or y == 0 or y == H-S
    elif level == 3:
        midx, midy = (W//2)//S*S, (H//2)//S*S
        return (S_range(x, midx, 1) and S_range(y, midy, 2)) or (S_range(y, midy, 1) and S_range(x, midx, 2))
    elif level >= 4:
        wall1 = (3*S <= x <= 7*S) and (y == 3*S or y == H-4*S)
        wall2 = (5*S <= y <= 9*S) and (x == W-5*S)
        return wall1 or wall2
    return False

def get_level_speed(level): 
    return BASE_SPEED + (level-1)*2

def get_username():
    name=""; active=True
    while active:
        win.fill(COLORS["LIGHT_GREEN"])
        draw_text("Username:", W//2-100,H//2-50)
        draw_text(name, W//2-100,H//2)
        draw_text("Press ENTER to continue", W//2-120,H//2+50)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); return None
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN and name: active=False
                elif e.key==pygame.K_BACKSPACE: name=name[:-1]
                elif e.key==pygame.K_ESCAPE: return None
                elif len(name)<15 and e.unicode.isalnum(): name+=e.unicode
    return name

def play():
    setup_db()
    username = get_username()
    if not username: return
    user_id = get_user_id(username)
    
    state = load_state(user_id)
    if state:
        score, level, snake_str, dir, food_pos_str, food_weight, food_lifetime = state
        snake = eval(snake_str)
        food = {"pos": eval(food_pos_str), "weight": food_weight, "lifetime": food_lifetime}
        win.fill(COLORS["LIGHT_GREEN"])
        draw_text(f"Welcome back, {username}!", W//2-100,H//2-30)
        draw_text(f"Level: {level}", W//2-80,H//2)
        draw_text("SPACE: continue saved(if you don't die)", W//2-150,H//2+30)
        draw_text("N: new game", W//2-150,H//2+60)
        pygame.display.update()
        waiting=True
        while waiting:
            for e in pygame.event.get():
                if e.type==pygame.QUIT: pygame.quit(); return
                if e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_SPACE: waiting=False
                    elif e.key==pygame.K_n:
                        snake=[(100,100),(80,100),(60,100)]
                        dir="RIGHT"
                        food=new_food(snake, 1)
                        score=0; level=1
                        waiting=False
    else:
        snake=[(100,100),(80,100),(60,100)]
        dir="RIGHT"
        food=new_food(snake, 1)
        score=0; level=1

    speed = get_level_speed(level)
    clock = pygame.time.Clock()
    run = True
    paused = False

    while run:
        now = time.time()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: run=False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    paused = not paused
                    if paused: save_state(user_id, score, level, snake, dir, food)
                if not paused:
                    if e.key == pygame.K_UP and dir != "DOWN": dir = "UP"
                    if e.key == pygame.K_DOWN and dir != "UP": dir = "DOWN"
                    if e.key == pygame.K_LEFT and dir != "RIGHT": dir = "LEFT"
                    if e.key == pygame.K_RIGHT and dir != "LEFT": dir = "RIGHT"

        if paused:
            draw_bg(level)
            draw_text("PAUSED - Game Saved", W//2-100,H//2-20,COLORS["RED"])
            draw_text("Press P to continue", W//2-80,H//2+10)
            pygame.display.update()
            continue

        draw_bg(level)
        hx, hy = snake[0]
        hx += {"LEFT":-S,"RIGHT":S,"UP":0,"DOWN":0}[dir]
        hy += {"UP":-S,"DOWN":S,"LEFT":0,"RIGHT":0}[dir]
        head = (hx, hy)

        if hx < 0 or hx >= W or hy < 0 or hy >= H or head in snake or is_wall(head, level):
            draw_bg(level)
            draw_text("Game Over!", W//2-70,H//2-20,COLORS["RED"])
            draw_text(f"Score: {score}", W//2-80,H//2+10)
            pygame.display.update()
            time.sleep(2)
            save_state(user_id, score, level, [], "", {"pos":(0,0),"weight":0,"lifetime":0})
            return

        snake.insert(0, head)
        if now > food["lifetime"]: food = new_food(snake, level)
        if head == food["pos"]:
            score += food["weight"]
            food = new_food(snake, level)
            if score >= level * 5:
                level += 1
                speed = get_level_speed(level)
        else:
            snake.pop()

        draw_snake(snake)
        draw_food(food)
        draw_text(f"Food: {max(0,int(food['lifetime']-now))}s",10,360,COLORS["RED"])
        draw_text(f"Score: {score}",10,10)
        draw_text(f"Level: {level}",500,10)
        draw_text(f"User: {username}",10,40)
        draw_text("Press P to pause/save",400,360,COLORS["BLACK"],small_font)
        pygame.display.update()
        clock.tick(speed)
play()