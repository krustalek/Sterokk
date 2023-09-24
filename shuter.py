from pygame import *
from random import randint
init()
mixer.music.load("songwar.mp3")  #музика
mixer.music.play(-1)
fire_sound = mixer.Sound('fire.ogg')

win_width = 700  #розмір вікна
win_height = 500

win = display.set_mode((win_width, win_height))
display.set_caption("War ny pochti Thunder")

background = transform.scale(image.load("Map.jpg"), (win_width, win_height)) #фон гри
clock = time.Clock()

lost = 0
score = 0
#клас гри
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()

        self.image = transform.scale(image.load(img), (w, h))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

    
class Player(GameSprite):  #Class зенітки
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            fire_sound.play()
            self.fire()

    def fire(self):  #Сняряди
        bul = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 15, 15)
        bullets.add(bul)

class Enemy(GameSprite):#ворог
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            lost += 1
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()


ship = Player("Zenitka.png", 5, win_height - 100, 80, 100, 8)

finish = False
run = True
FPS = 60

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(5):
    x = randint(80, win_width - 80)
    speed = randint(1, 2)
    monster = Enemy("Su-25.png", x, -40, 80, 50, speed)
    monsters.add(monster)


f = font.Font(None,45)  

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        win.blit(background, (0, 0))

        text_score = f.render(f"Рахунок: {score}", True, (255,255,255))
        win.blit(text_score, (10,20))

        text_lost = f.render(f"Пропущено: {lost}", True, (255,255,255))
        win.blit(text_lost, (10,50))

        monsters.update()
        bullets.update()


        ship.update()
        ship.reset()
        monsters.draw(win)
        bullets.draw(win)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            x = randint(80, win_width - 80)
            speed = randint(1, 2)
            monster = Enemy("Su-25.png", x, -40, 80, 30, speed)
            monsters.add(monster)

        if sprite.spritecollide(ship,monsters, False) or lost >= 10: 
            finish = True 
            lose = f.render("Слив катку,бот",True, (200, 50, 50))
            win.blit(lose, (200,200))

        if score >=16:
            finish = True 
            lose = f.render("Winner winner chiken diner",True, (255, 150, 0))
            win.blit(lose, (200,200))

    display.update()
    clock.tick(FPS)