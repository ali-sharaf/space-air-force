import pygame 
import os

from pygame.constants import K_a
pygame.font.init()
UH = (95, 80)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 150)
VEL = 5

BLACK = (0, 0, 0)

BULLET_VEL = 20

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
WIDTH, HEIGHT = 1955, 1000
WHITE = (255, 255, 255)
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Space Airphorce")
FPS = 100
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT)) 
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (95, 80)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (95, 80)), -90)
yellow = pygame.Rect((300, 500), UH)
red = pygame.Rect((1300, 500), UH)
BORDER = pygame.Rect(WIDTH//2- 5, 0, 10, HEIGHT)
MAX_BULLETS = 5


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text =HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text,(10, 10))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a]and yellow.x - VEL > 0:    
        yellow.x -= VEL
    if key_pressed[pygame.K_d]and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if key_pressed[pygame.K_w]and yellow.y - VEL > 0:
        yellow.y -= VEL
    if key_pressed[pygame.K_s]and yellow.y + VEL + yellow.height < HEIGHT - 15:
        yellow.y += VEL

def red_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT]and red.x - VEL > BORDER.x + BORDER.width:    
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT]and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if key_pressed[pygame.K_UP]and red.y - VEL > 0:
        red.y -= VEL
    if key_pressed[pygame.K_DOWN]and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL
        
  
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > 1700:
            yellow_bullets.remove(bullet)    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
       
        
        
        
        
        elif bullet.x < 0:
            red_bullets.remove(bullet)
            
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    clock=pygame.time.Clock()
    pygame.init()
    print(pygame.get_init)
    red_bullets = []
    yellow_bullets = []
    red_health = 100
    yellow_health = 100
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        key_pressed = pygame.key.get_pressed()
        yellow_movement(key_pressed, yellow)
        red_movement(key_pressed, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        if event.type == RED_HIT:
            red_health -=1

        if event.type == YELLOW_HIT:
            yellow_health -=1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 20, 10)
                yellow_bullets.append(bullet)
            if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:         
                bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 20, 10)
                red_bullets.append(bullet)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
      
                
        winner_text = ""
        if yellow_health <= 0:
            winner_text = "red wins"


        if red_health <= 0:
            winner_text = "yellow wins"
        if winner_text != "":
            draw_winner(winner_text)
                                
    pygame.quit()

 

if __name__ == "__main__":
    main()

