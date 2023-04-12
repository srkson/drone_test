import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
dt = 0
running = True

# PLAYER IMAGE

DEFAULT_IMAGE_SIZE = (50, 50)

#img = pygame.image.load('drone.png')
#img = pygame.transform.scale(img, DEFAULT_IMAGE_SIZE)


# PLAYER
class Player:

    def __init__(self, x, y, w=50, h=50):
        
        self.x = int(x)
        self.y = int(y)
        self.w = w
        self.h = h
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.max_speed = 8
        self.step = 0.3
        self.acc = 0.9
        self.angle = 0
        self.angle_step = 1.5
        self.max_angle = 45
        self.score = 0
        # break
        self.image = pygame.image.load('drone.png')
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)
        
        
        self.color = (100, 100, 100)

    def draw(self, screen):
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        screen.blit(pygame.transform.rotate(self.image, self.angle), self.rect) # (self.x, self.y)
        #pygame.draw.rect(screen, self.color, self.rect)
        #pygame.transform.rotate(img, self.angle)

    def update(self):
        
        if self.left_pressed and not self.right_pressed:
            self.velX = max(self.velX - self.step, -self.max_speed)
            self.angle = min(self.angle + self.angle_step, self.max_angle)
            if self.x < 10:
                self.velX = 0

        elif self.right_pressed and not self.left_pressed:
            self.velX = min(self.velX + self.step, self.max_speed)
            self.angle = max(self.angle - self.angle_step, -self.max_angle)
            if self.x + self.h > WIDTH - 10:
                self.velX = 0

        else:
            self.velX *= self.acc
            self.angle *= self.acc

        if self.up_pressed and not self.down_pressed:
            self.velY = max(self.velY - self.step, - self.max_speed)
            if self.y < 10:
                self.velY = 0

        elif self.down_pressed and not self.up_pressed:
            self.velY = min(self.velY + self.step, self.max_speed)
            if self.y + self.h > HEIGHT - 10:
                self.velY = 0

        else:
            self.velY *= self.acc

        self.x += self.velX
        self.y += self.velY




font = pygame.font.Font(None, 36)


# if player.x > target.x and player.x < target.x + target.w and player.y > target.y and player.y < target.y + target.h:


# TARGET

class Target:

    def __init__(self, x, y, w=30, h=30):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = (250, 160, 50)
        self.rect = pygame.Rect((self.x, self.y), (self.w, self.h))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)



        

# INIT PLAYER
player = Player(random.randint(100, WIDTH - 100),
                random.randint(100, HEIGHT - 100))
#target = Target(400, 400)

target_list = []
def generateTargets():
    for i in range(5):
        target_list.append(Target(random.randint(
            100, WIDTH - 100), random.randint(100, HEIGHT - 100)))



def detectCollision():
    '''if player.x > targets.x and player.x < targets.x + targets.w and player.y > targets.y and player.y < targets.y + targets.h:
            target_list.remove(targets)
            player.score += 1
    '''
    global target_list
    for target in target_list:
        collide = pygame.Rect.colliderect(player.rect, target.rect)
        if collide:
            target_list.remove(target)
            target_list.append(Target(random.randint(
            100, WIDTH - 100), random.randint(100, HEIGHT - 100)))
            print("COLLIDES!")
            player.score += 1
        #target_list.remove(target)
        
        
            
            
            
            
            
            
            
# MAIN LOOP




while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            player.up_pressed = False
            player.down_pressed = False
            player.right_pressed = False
            player.left_pressed = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.up_pressed = True
    if keys[pygame.K_s]:
        player.down_pressed = True
    if keys[pygame.K_a]:
        player.left_pressed = True
    if keys[pygame.K_d]:
        player.right_pressed = True

    screen.fill('gray')
    
    if len(target_list) == 0:
        generateTargets()
    
    for target in target_list:
        target.draw(screen)
    player.update()
    player.draw(screen)

    detectCollision()

    score_text = font.render(f'Score: {player.score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    dt = clock.tick(60) / 1000
