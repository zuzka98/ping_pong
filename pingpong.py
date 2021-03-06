import pygame

pygame.init()

window_width = 600
window_height = 420
game_over = False
p_score = 0
c_score = 0

window_game = pygame.display.set_mode((window_width, window_height))

clock = pygame.time.Clock()

play_again_img = pygame.image.load('play_again.jpeg').convert_alpha()


class Ball:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.color = '#823FF3'

    def draw(self):
        pygame.draw.circle(window_game, self.color, [self.x, self.y], self.r)


class Racket:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = 'black'

    def draw(self):
        pygame.draw.rect(window_game, self.color, [self.x, self.y, self.w, self.h])


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                game_init()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        window_game.blit(self.image, (self.rect.x, self.rect.y))


class Text:
    def __init__(self, text, coordinates):
        self.name = 'freesansbold.ttf'
        self.size = 20
        self.text = text
        self.color = 'black'
        self.coordinates = coordinates

    def show_player(self):
        font = pygame.font.Font(self.name, self.size)
        text = font.render(self.text + str(p_score), True, self.color)
        rect = text.get_rect()
        rect.center = self.coordinates
        window_game.blit(text, rect)

    def show_computer(self):
        font = pygame.font.Font(self.name, self.size)
        text = font.render(self.text + str(c_score), True, self.color)
        rect = text.get_rect()
        rect.center = self.coordinates
        window_game.blit(text, rect)


def game_init():
    global ball, dx, dy
    global game_over, speed
    ball.x, ball.y = window_width / 2, window_height / 2
    dx = 1
    dy = 0
    speed = 0
    ball.x += dx
    ball.y += dy
    game_over = False


def stop_game():
    global game_over
    game_over = True
    play_again_button.draw()


def count_dy_after_hit():
    global dy
    distance = round((racket_left.y + racket_left.h / 2) - ball.y)
    angle = (distance * 1 / 40) * -1
    dy = angle
    return dy


player_score = Text('You: ', (100, 50))
computer_score = Text('Computer: ', (500, 50))

ball = Ball(window_width / 2, window_height / 2, 8)
play_again_button = Button(window_width / 2, window_height / 2, play_again_img)

racket_left = Racket(0, window_height / 2, 10, 45)
racket_right = Racket(int(window_width - 10), int(window_height / 2), 10, 45)

dx = 1
dy = 0

running = True
while running:

    window_game.fill((255, 255, 255))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            mouse_position = pygame.mouse.get_pos()
            racket_left.y = mouse_position[1] - racket_left.h / 2

            if mouse_position[1] >= window_height - racket_left.h/2:
                racket_left.y = window_height - 80

    # right racket movement
    racket_right.y = ball.y - racket_right.h / 2

    # right racket crossing lower border
    if racket_right.y + (racket_right.h / 2) >= window_height - racket_right.h / 2:
        racket_right.y = window_height - racket_right.h

    # right racket crossing upper border
    if racket_right.y <= 0:
        racket_right.y = 0

    # left racket crossing upper border
    if racket_left.y <= 0:
        racket_left.y = 0

    if game_over:
        stop_game()
    else:
        ball.x -= dx
        ball.y += dy

        hit_right_racket = ball.x == racket_right.x
        if hit_right_racket:
            dx = dx * (-1)

        # hit_left_racket
        if ball.x == racket_left.w and (ball.y >= racket_left.y and ball.y < racket_left.y + racket_left.h):
            dx = dx * (-1)
            count_dy_after_hit()

        upper_edge_crossed = ball.y < 0
        if upper_edge_crossed:
            dy = dy * (-1)

        lower_edge_crossed = ball.y > window_height
        if lower_edge_crossed:
            dy = dy * (-1)

        left_edge_crossed = ball.x <= 0
        if left_edge_crossed:
            stop_game()
            c_score += 1

        right_edge_crossed = ball.x >= window_width
        if right_edge_crossed:
            stop_game()
            p_score += 1

        ball.draw()

    racket_left.draw()
    racket_right.draw()
    pygame.draw.line(window_game, 'grey', (window_width / 2, 0), (window_width / 2, window_height), width=1)
    player_score.show_player()
    computer_score.show_computer()
    pygame.display.flip()

pygame.quit()
