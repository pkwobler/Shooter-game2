from pygame import *
from random import randint
from time import time as timer
font.init()
font1 = font.Font(None, 45)

#экран
win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode(
    (win_width, win_height)
)

win = font1.render('You win!!!', True, (255, 255, 255))
lose = font1.render('You loseeeeee!', True, (180, 0, 0))

max_lost = 3

#картинка
galaxy = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))


#классы
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x,  player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys [K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_width - 65:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


lost = 0
score = 0
score2 = 10

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed  + randint (0, 5)
        global lost
        if self.rect.y >= win_height:
            self.rect.y = 0
            self.rect.x = randint(0, win_width - 60)
            lost = lost + 1

class Bullet(GameSprite):
   def update(self):
       self.rect.y += self.speed
       if self.rect.y < 0:
           self.kill()


#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#игрок
player = Player('rocket.png', 5, win_height -100, 65, 65, 10)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1, 6):
   monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 6):
   asteroid = Enemy('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   asteroids.add(asteroid)

num_fire = 0 
rel_time = False



#цикл
game = True
finish = False
space = mixer.Sound('space.ogg')
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
        elif e.type == KEYDOWN:
            if e.key == K_SPACE: 
                # проверка времени для перезарядки пуль каждые 3 секунды
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1 
                    fire_sound.play()
                    player.fire()
                    print(num_fire)
                     
                if num_fire >= 5 and rel_time == False: 
                    last_time = timer() #засекаем время, когда это произошло
                    rel_time = True #ставим флаг перезарядки
                        

    
    if not finish:
        window.blit(galaxy, (0, 0))
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 20))
        text = font1.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 50))
        player.reset()
        player.update()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        space.play()
        asteroids.update()
        asteroids.draw(window)





        #столкновение спрайтов
        sprite_list = sprite.spritecollide(player, monsters, False)
        if lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        
        if score > score2:
            finish = True
            window.blit(win, (200, 200))



        #перезарядка
        if rel_time == True:
            now_time = timer() #считываем время

            if now_time - last_time < 3: #пока не прошло 3 секунды выводим информацию о перезаряд
                reload = font1.render('Wait, reload…', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False #сбрасываем флаг


        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for c in sprite_list  :
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
    display.update()
    time.delay(50)
