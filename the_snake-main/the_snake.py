from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 14

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(snake):
    """Управление змейкой, через нажатие клавиш."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake.direction != DOWN:
        snake.next_direction = UP
    elif keys[pygame.K_DOWN] and snake.direction != UP:
        snake.next_direction = DOWN
    elif keys[pygame.K_LEFT] and snake.direction != RIGHT:
        snake.next_direction = LEFT
    elif keys[pygame.K_RIGHT] and snake.direction != LEFT:
        snake.next_direction = RIGHT


class GameObject:
    """Базовый класс."""

    def __init__(self, body_color=None,
                 position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        """Определение позиции и цвета тела."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки игрового объекта."""
        pass


class Apple(GameObject):
    """Класс, где прописан объект яблоко."""

    def __init__(self):
        """Определение позиции и цвета тела."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """
        Метод случайной генерации позиции
        яблока внутри сетки игрового поля.

        """
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Метод отрисовки яблока на экране."""
        pygame.draw.rect(screen, self.body_color, (self.position[0],
                         self.position[1], GRID_SIZE, GRID_SIZE))


class Snake(GameObject):
    """Класс, где прописан объект змейка."""

    def __init__(self):
        """Определение позиции,направления, длины тела, цвета тела."""
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Метод обновления направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """
        Метод перемещения змейки на одну ячейку в
        соответствии с текущим направлением.
        """
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Метод прорисовки змейки."""
        pygame.draw.rect(screen, self.body_color,
                         (self.positions[0][0], self.positions[0][1],
                          GRID_SIZE, GRID_SIZE))
        for position in self.positions:
            pygame.draw.rect(screen, self.body_color,
                             (position[0], position[1],
                              GRID_SIZE, GRID_SIZE))

    def get_head_position(self, apple=None):
        """Возвращает голову."""
        return self.positions[0][0], self.positions[0][1]

    def reset(self):
        """Метод сброса змейки до начального состояния."""
        self.__init__()

    def is_snake_collision(self):
        """Проверка столкновения головы змейки со своим телом."""
        head = self.positions[0]
        body = self.positions[1:]
        return head in body
    
    def count_score(self, score=0):
        self.score = score + 1
        return score

def main():
    """Основная функция, где прописана логика игры."""
    score = 0
    font_score = pygame.font.Font(None, 36)
    snake = Snake()
    apple = Apple()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.count_score()

        if snake.is_snake_collision():
            snake.reset()
            score = 0
        if snake.get_head_position() == tuple(apple.position):
            snake.length += 1
            score += 1
            apple.randomize_position()
        
        screen.fill(BOARD_BACKGROUND_COLOR)

        pygame.draw.rect(screen, BORDER_COLOR,
                         (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 20)

        snake.draw()
        apple.draw()

        text = font_score.render(f'Съедено яблок: {score}.', True, (47, 79, 79))
        place = text.get_rect(center=(150, 10))
        screen.blit(text, place)

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == "__main__":
    main()
