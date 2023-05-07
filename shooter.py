import random
import pygame
pygame.init()
 
clock = pygame.time.Clock()
FPS = 40
count_killed = 0
count_lost = 0

background = pygame.transform.scale(pygame.image.load('background.jpg'), (800,750))

window = pygame.display.set_mode((800,750))
pygame.display.set_caption('Шутер')

pygame.mixer.music.load('music.mp3')
pygame.mixer_music.play()

enemy_death = pygame.mixer.Sound('enemy_death.mp3')

bullets = []

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, size_x, size_y, speed):
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x >= 5:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x <= 750:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT] and self.rect.x >= 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x <= 750:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE]:
            self.fire()
    def fire(self):
        bullet = Bullet('bullet.png', rocket.rect.x + 12, rocket.rect.y - 18, 7, 20, -5)
        bullets.append(bullet)
class Enemy(GameSprite):
    def update(self):
        global count_lost
        self.rect.y += self.speed
        if self.rect.y >= 750:
            count_lost += 1
            self.rect.y = random.randint(-300, -100)
            self.rect.x = random.randint(0,750)
            self.speed = random.uniform(2,4)
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 10:
            bullets.remove(self)
            return True

rocket = Player('rocket.png', 350, 600, 44, 100, 5)

enemies = []
for i in range(5):
    ufo = Enemy('ufo.png', random.randint(0,750), random.randint(-300, -100), 52, 50, random.uniform(2,4))
    enemies.append(ufo)

def win():
    text_win = pygame.font.Font(None, 100).render('Ти вийграв :)', True, (0,255,0))
    window.blit(text_win, (180,320))
def lose():
    text_not_win = pygame.font.Font(None, 100).render('Ти програв :(', True, (255,0,0))
    window.blit(text_not_win, (180,320))
    
game = True
update = True
while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False

    window.blit(background, (0,0))

    rocket.reset()
    text_killed = pygame.font.Font(None, 40).render('Вбито: ' + str(count_killed), True, (255,0,0))
    text_lost = pygame.font.Font(None, 40).render('Пропущено: ' + str(count_lost), True, (255,0,0))
    window.blit(text_killed, (10,10))
    window.blit(text_lost, (10,50))

    if count_killed >= 10:
        win()
        update = False
        enemies.clear()
    if count_lost >= 10:
        lose()
        update = False
        enemies.clear()
    for i in enemies:
        i.reset()
        if rocket.rect.colliderect(i.rect):  
            lose()   
            update = False
            enemies.clear()
            enemies.append(i)

    if update:
        rocket.update()
        for i in enemies:
            i.update()
            if rocket.rect.colliderect(i.rect):
                lose()
                update = False
        for bullet in bullets:
            bullet.reset()
            v=bullet.update()
            if v:
                continue
            for enemy in enemies:
                if enemy.rect.colliderect(bullet.rect):
                    enemy_death.play()
                    count_killed += 1
                    bullets.remove(bullet)
                    enemy.rect.x = random.randint(0,750)
                    enemy.rect.y = random.randint(-300, -100)
                    enemy.speed = random.uniform(2,4)
                    break
    pygame.display.update()
    clock.tick(FPS)