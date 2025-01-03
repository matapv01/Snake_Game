import pygame
import random
import time

# Khởi tạo pygame
pygame.init()

# Màu sắc
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (128, 0, 128)  # Màu cho mồi đặc biệt

# Kích thước cửa sổ
width = 600
height = 400
screen = pygame.display.set_mode((width, height))

# Tên game
pygame.display.set_caption('Snake Game')

# Đồng hồ điều chỉnh tốc độ khung hình
clock = pygame.time.Clock()

# Kích thước thân rắn và tốc độ ban đầu
snake_block = 10
initial_speed = 15
speed_increment = 0.5  # Tăng tốc độ mỗi khi rắn dài thêm 5 đoạn

# Font chữ
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def show_score(score):
    value = score_font.render("Your Score: " + str(score), True, black)
    screen.blit(value, [0, 0])

def draw_snake(snake_block, snake_list):
    # Vẽ đầu rắn
    pygame.draw.rect(screen, red, [snake_list[0][0], snake_list[0][1], snake_block, snake_block])
    # Vẽ thân rắn
    for x in snake_list[1:]:
        pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block])

def draw_food(x, y, color, shape='rect'):
    if shape == 'circle':
        pygame.draw.circle(screen, color, (int(x + snake_block / 2), int(y + snake_block / 2)), int(snake_block / 2))
    elif shape == 'star':
        pygame.draw.polygon(screen, color, [
            (x + snake_block / 2, y),  # top
            (x + snake_block * 0.6, y + snake_block * 0.4),  # right
            (x + snake_block, y + snake_block * 0.4),  # bottom right
            (x + snake_block * 0.7, y + snake_block * 0.6),  # bottom left
            (x + snake_block * 0.8, y + snake_block),  # bottom
            (x + snake_block / 2, y + snake_block * 0.8),  # left bottom
            (x + snake_block * 0.2, y + snake_block),  # top left
            (x, y + snake_block * 0.6),  # top right
            (x + snake_block * 0.2, y + snake_block * 0.4),  # top
            (x + snake_block / 2, y)  # back to top
        ])
    else:
        pygame.draw.rect(screen, color, [x, y, snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])

def generate_food():
    return round(random.randrange(0, width - snake_block) / 10.0) * 10.0, round(random.randrange(0, height - snake_block) / 10.0) * 10.0

def gameLoop():  # Hàm chính điều khiển game
    global snake_speed  # Khai báo biến snake_speed là biến toàn cục để có thể thay đổi nó trong gameLoop()

    snake_speed = initial_speed  # Khởi tạo tốc độ ban đầu
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    # Không cho rắn đi lùi
    last_direction = None

    snake_list = []
    length_of_snake = 1

    # Tọa độ mồi thường
    foodx, foody = generate_food()
    food_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    food_time = time.time()

    # Tọa độ mồi đặc biệt
    special_foodx = None
    special_foody = None
    special_food_active = False
    special_food_timer = 0
    special_food_duration = 200  # Thời gian tồn tại của mồi đặc biệt (đơn vị khung hình)

    score = 0

    while not game_over:

        while game_close:
            screen.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            show_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and last_direction != 'RIGHT':
                    x1_change = -snake_block
                    y1_change = 0
                    last_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and last_direction != 'LEFT':
                    x1_change = snake_block
                    y1_change = 0
                    last_direction = 'RIGHT'
                elif event.key == pygame.K_UP and last_direction != 'DOWN':
                    x1_change = 0
                    y1_change = -snake_block
                    last_direction = 'UP'
                elif event.key == pygame.K_DOWN and last_direction != 'UP':
                    x1_change = 0
                    y1_change = snake_block
                    last_direction = 'DOWN'

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(blue)
        
        # Xử lý mồi thường
        if time.time() - food_time < (10 - length_of_snake / 20):  # Thời gian tồn tại của mồi thường
            draw_food(foodx, foody, food_color, shape='circle')
        else:
            foodx, foody = generate_food()
            food_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            food_time = time.time()

        # Xử lý mồi đặc biệt
        if special_food_active:
            draw_food(special_foodx, special_foody, yellow, shape='star')
            special_food_timer -= 1
            if special_food_timer <= 0:
                special_food_active = False

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Kiểm tra va chạm với thân rắn sau khi cập nhật vị trí
        if len(snake_list) > 1 and snake_head in snake_list[:-1]:
            game_close = True

        draw_snake(snake_block, snake_list)
        show_score(score)

        pygame.display.update()

        # Xử lý khi ăn mồi thường
        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food()
            food_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            food_time = time.time()
            length_of_snake += 1
            score += 10

            # Tăng tốc độ khi rắn dài hơn
            snake_speed = initial_speed + (length_of_snake // 5) * speed_increment

            # Xác suất xuất hiện mồi đặc biệt (10%)
            if not special_food_active and random.randint(1, 10) == 1:
                special_foodx, special_foody = generate_food()
                special_food_active = True
                special_food_timer = int(200 - (length_of_snake * 2))  # Thời gian tồn tại mồi đặc biệt giảm dần

        # Xử lý khi ăn mồi đặc biệt
        if special_food_active and x1 == special_foodx and y1 == special_foody:
            special_food_active = False
            length_of_snake += 2
            score += 50

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
