import pygame
import random

# Константы
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
WHITE, GREEN, RED, BLUE = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Функция для генерации еды в случайном месте, избегая змеи
def generate_food(snake):
    while True:
        food_x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        food_y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if (food_x, food_y) not in snake:
            return food_x, food_y

# Инициализация змейки и еды
snake = [(100, 100)]
direction = (CELL_SIZE, 0)
food = generate_food(snake)
score, level, speed = 0, 1, 5

running = True
while running:
    screen.fill(WHITE)
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)
    
    # Движение змейки
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])
    
    # Проверка на столкновение со стеной
    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        running = False
    
    # Проверка на столкновение с самой собой
    if new_head in snake:
        running = False
    
    snake.insert(0, new_head)
    
    # Проверка на поедание еды
    if new_head == food:
        score += 1
        food = generate_food(snake)
        
        # Повышение уровня каждые 3 очка
        if score % 3 == 0:
            level += 1
            speed += 1
    else:
        snake.pop()
    
    # Отрисовка змейки и еды
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))
    
    # Отображение счета и уровня
    score_text = font.render(f"Score: {score}  Level: {level}", True, BLUE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
