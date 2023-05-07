import pygame,sys,random
from pygame.math import Vector2

pygame.mixer.pre_init()
pygame.init()

pygame.display.set_caption("Snake Game")

class FRUIT:
    def __init__(self):
        self.randomize()
        self.apple = pygame.transform.scale(pygame.image.load("Graphics/apple.png"),(cell_size,cell_size)).convert_alpha()
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size,self.pos.y * cell_size,cell_size,cell_size)
        screen.blit(self.apple,fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up = pygame.transform.scale(pygame.image.load("Graphics/head_up.png"),(cell_size,cell_size)).convert_alpha()
        self.head_down = pygame.transform.scale(pygame.image.load("Graphics/head_down.png"),(cell_size,cell_size)).convert_alpha()
        self.head_right = pygame.transform.scale(pygame.image.load("Graphics/head_right.png"),(cell_size,cell_size)).convert_alpha()
        self.head_left = pygame.transform.scale(pygame.image.load("Graphics/head_left.png"),(cell_size,cell_size)).convert_alpha()

        self.tail_up = pygame.transform.scale(pygame.image.load("Graphics/tail_up.png"),(cell_size,cell_size)).convert_alpha()
        self.tail_down = pygame.transform.scale(pygame.image.load("Graphics/tail_down.png"),(cell_size,cell_size)).convert_alpha()
        self.tail_right = pygame.transform.scale(pygame.image.load("Graphics/tail_right.png"),(cell_size,cell_size)).convert_alpha()
        self.tail_left = pygame.transform.scale(pygame.image.load("Graphics/tail_left.png"),(cell_size,cell_size)).convert_alpha()

        self.body_bottomleft = pygame.transform.scale(pygame.image.load("Graphics/body_bottomleft.png"),(cell_size,cell_size)).convert_alpha()
        self.body_bottomright = pygame.transform.scale(pygame.image.load("Graphics/body_bottomright.png"),(cell_size,cell_size)).convert_alpha()
        self.body_horizontal = pygame.transform.scale(pygame.image.load("Graphics/body_horizontal.png"),(cell_size,cell_size)).convert_alpha()
        self.body_vertical = pygame.transform.scale(pygame.image.load("Graphics/body_vertical.png"),(cell_size,cell_size)).convert_alpha()
        self.body_topleft = pygame.transform.scale(pygame.image.load("Graphics/body_topleft.png"),(cell_size,cell_size)).convert_alpha()
        self.body_topright = pygame.transform.scale(pygame.image.load("Graphics/body_topright.png"),(cell_size,cell_size)).convert_alpha()

        self.eat_sound = pygame.mixer.Sound("Sounds/Eating_sound.wav")

    def draw_snake(self):
        self.update_head_direction()
        self.update_tail_direction()

        for index,block in enumerate(self.body):
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index - 1] - block
                next_block = self.body[index + 1] - block

                if previous_block.x == next_block.x :
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y :
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1 :
                        screen.blit(self.body_topleft,block_rect)
                    elif previous_block.y == -1 and next_block.x == 1 or previous_block.x == 1 and next_block.y == -1 :
                        screen.blit(self.body_topright,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1 :
                        screen.blit(self.body_bottomleft,block_rect)
                    elif previous_block.y == 1 and next_block.x == 1 or previous_block.x == 1 and next_block.y == 1 :
                        screen.blit(self.body_bottomright,block_rect)

    def update_head_direction(self):
        head_relation = self.body[1] - self.body[0]

        if head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(0,-1): self.head = self.head_down
        elif head_relation == Vector2(0,1): self.head = self.head_up

    def update_tail_direction(self):
        tail_relation = self.body[-2] - self.body[-1]

        if tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
    
    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

    def play_eat_sound(self):
        self.eat_sound.play()

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.eat_fruit()
        self.check_collision()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def eat_fruit(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.add_block()
            self.fruit.randomize()
            self.snake.play_eat_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_collision(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number :
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,green,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,green,grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = font.render(score_text,True,black)
        score_x = cell_number * cell_size - 60
        score_y = cell_number * cell_size - 40
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = self.fruit.apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

        pygame.draw.rect(screen,l_green,bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(self.fruit.apple,apple_rect)
        pygame.draw.rect(screen,black,bg_rect,2)

# create screen
cell_size = 20
cell_number = 30
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))

# colors
white = (255,255,255)
green = (125,255,125)
l_green = (150,255,150)
l_red = (255,150,150)
black = (0,0,0)

# frames per second
fps = 60
clock = pygame.time.Clock()

font = pygame.font.Font("Fonts/Poetsenone.ttf",17)

Screen_Update = pygame.USEREVENT
pygame.time.set_timer(Screen_Update,150)

main_game = MAIN()
# create game loop
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == Screen_Update:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
    
    screen.fill(l_green)
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(fps)