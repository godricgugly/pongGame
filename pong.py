from random import randint
import pygame

pygame.init()

size = (700, 500)
FPS = 50

class colors:
    blue = (000, 000, 255)
    black = (000, 000, 000)
    red = (255, 000, 000)
    green = (000, 255, 000)
    white = (255, 255, 255)

player1name = input("player1: ")
player1Name = player1name + "   "
player1color = colors.green


player2name = input("player2: ")
player2Name = "   " + player2name
player2color = colors.blue

ballColor = colors.red
ballSize = 7

class Ball(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(colors.black)
        self.image.set_colorkey(colors.black)
        self.color = color
        pygame.draw.circle(self.image, self.color, (width // 2, height // 2), ballSize)
        self.velocity = [randint(4, 8), randint(-8, 8)]
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8, 8)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(colors.black)
        self.image.set_colorkey(colors.black)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
    def moveUp(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 68:
            self.rect.y = 68

    def moveDown(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 396:
            self.rect.y = 396

pygame.display.set_caption("pong")
screen = pygame.display.set_mode(size)

paddleA = Paddle(player1color, 10, 100)
paddleA.rect.x = 20
paddleA.rect.y = 200
paddleB = Paddle(player2color, 10, 100)
paddleB.rect.x = 670
paddleB.rect.y = 200

ball = Ball(ballColor, ballSize*2, ballSize*2)
ball.rect.x = 345
ball.rect.y = 195

reverseBallDirectionAfterScore = -ball.velocity[0]

all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

playing = True

clock = pygame.time.Clock()

scoreA = 0
scoreB = 0

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    if pygame.time.get_ticks() < 1000:
        pygame.time.delay(50)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(5)
    if keys[pygame.K_s]:
        paddleA.moveDown(5)
    if keys[pygame.K_UP]:
        paddleB.moveUp(5)
    if keys[pygame.K_DOWN]:
        paddleB.moveDown(5)

    all_sprites_list.update()

    if ball.rect.x >= 690:
        ball.rect.x = 345
        ball.rect.y = 195
#        ball.velocity[0] = reverseBallDirectionAfterScore # optional
        scoreA += 1
    if ball.rect.x <= 0:
#        ball.velocity[0] = reverseBallDirectionAfterScore # optional
        ball.rect.x = 345
        ball.rect.y = 195
        scoreB += 1
    if ball.rect.y > 500-ballSize*2:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 70:
        ball.velocity[1] = -ball.velocity[1]

    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
        ball.bounce()

    screen.fill(colors.black)
    pygame.draw.line(screen, colors.white, [0, 498], [700, 498], 5)
    pygame.draw.line(screen, colors.white, [0, 65], [700, 65], 5)
    pygame.draw.line(screen, colors.white, [349, 0], [349, 500], 5)
    all_sprites_list.draw(screen)

    font = pygame.font.Font(None, 74)
    playerText = font.render(player1Name, 1, player1color)
    scoreText = font.render(str(scoreA), 1, colors.white)
    screen.blit(playerText, (10, 10))
    screen.blit(scoreText, (250, 10))

    playerText = font.render(player2Name, 1, player2color)
    scoreText = font.render(str(scoreB), 1, colors.white)
    screen.blit(playerText, (450, 10))
    screen.blit(scoreText, (415, 10))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

if scoreA > scoreB:
    print("The winner is:", player1name, "!!!")
if scoreA < scoreB:
    print("The winner is:", player2name, "!!!")
if scoreA == scoreB:
    print("It's a draw!")
