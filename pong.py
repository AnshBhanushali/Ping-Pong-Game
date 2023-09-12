import pygame
pygame.init()

WIDTH, HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game Window")

FPS = 60

GREEN = (0,100,0)
WHITE = (255,255,255)
RED = (255,0,0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 10

class Paddle:
    COLOR1 = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR1, (self.x,self.y, self.width, self.height))
 

    
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

class Ball:
    max_vel = 5
    COLOR = RED

    def __init__(self, x, y, radius):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = self.max_vel
        self.y_vel = 0


    def draw(self, win):
        pygame.draw.circle(win, self.COLOR,(self.x, self.y),self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel = self.max_vel




def draw(WINDOW, paddles, ball, left_score, right_score):
    WINDOW.fill(GREEN)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    
    WINDOW.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    WINDOW.blit(right_score_text, (3*WIDTH//4 - right_score_text.get_width()//2, 20))
    
    for paddle in paddles:
        paddle.draw(WINDOW)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(WINDOW, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(WINDOW)
    pygame.display.update()


def handle_ball_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x - ball.radius <= left_paddle.x + left_paddle.width and \
            left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
        ball.x_vel = abs(ball.x_vel)
        relative_y= (ball.y - left_paddle.y) / left_paddle.height
        ball.y_vel = -ball.max_vel * relative_y

    if ball.x + ball.radius >= right_paddle.x and \
            right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
        ball.x_vel = -abs(ball.x_vel)  
        relative_y = (ball.y - right_paddle.y) / right_paddle.height
        ball.y_vel = -ball.max_vel * relative_y
 


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH-10 - PADDLE_WIDTH,HEIGHT//2 - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WINDOW, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys,left_paddle,right_paddle)
        handle_ball_collision(ball, left_paddle, right_paddle)
        ball.move()
        
        if ball.x < 0:
            right_score +=1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True

        elif right_score >= WINNING_SCORE:
            won = True

        if won:
            text = SCORE_FONT.render("PLAYER WON", 1, WHITE)
            WINDOW.blit(text,(WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()

if __name__ == '__main__':
    main()
