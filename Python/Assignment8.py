import pygame
import numpy
import time

from pygame.locals import*
from time import sleep

class Sprite():
        def __init__(self,x,y,w,h,image_url,model):
                self.x = x
                self.y = y
                self.w = w
                self.h = h
                self.image_url = image_url
                self.model = model
                self.image = pygame.image.load(image_url)

class Fireball(Sprite):
        def __init__(self,x,y,w,h,image_url,model):
                self.x = x
                self.y = y
                self.model = model
                super().__init__(x,y,w,h,image_url,model)
                self.type = "fireball"
                self.vert_velocity = 10
                self.flip = False

                if(self.model.mario.flip == False):
                        self.direction = 1
                        self.flip = False
                if(self.model.mario.flip == True):
                        self.direction = -1
                        self.flip = True

        def update(self):
                self.x += (12 * self.direction)

                self.vert_velocity += 2.5
                self.y += self.vert_velocity

                if(self.y > 535):
                        self.vert_velocity = -22

                if(self.y < 0):
                        self.y = 0
                

class Goomba(Sprite):
        def __init__(self,x,y,w,h,image_url,model):
                self.x = x
                self.y = y
                self.w = w
                self.h = h
                self.image_url = image_url
                self.model = model
                self.type = "goomba"
                super().__init__(x,y,w,h,image_url,model)
                self.speed = 10
                self.direction = 1
                self.numFramesOnFire = 0
                self.isOnFire = False
                self.dead = False
                self.flip = False

        def update(self):
                self.prev_x = self.x

                if self.isOnFire == False:
                        self.x += self.speed*self.direction

                if self.isOnFire == True:
                        self.numFramesOnFire += 5
                        
                if self.numFramesOnFire >= 200:
                        self.dead = True

                if self.isOnFire == True:
                        self.image = pygame.image.load("goomba_fire.png")
                else:
                        self.image = pygame.image.load(self.image_url)

        def getOutOfSprite(self,s):
                if((self.x+self.w)>=s.x and (self.prev_x +self.w)<=s.x):
                        self.x = (s.x-self.w)
                        self.direction = self.direction*(-1)
                        self.flip = True

                if(self.x < (s.x+s.w) and self.prev_x >= (s.x+s.w)):
                        self.x = (s.x+s.w)
                        self.direction = self.direction*(-1)
                        self.flip = False
                        

class Tube(Sprite):
        def __init__(self,x,y,w,h,image_url,model):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.image_url = image_url
            self.model = model
            self.type = "tube"
            super().__init__(x,y,w,h,image_url,model)
            self.flip = False

        def update(self):
                z = 0

class Mario(Sprite):
        def __init__(self,x,y,w,h,image_url,model):
                self.x = x
                self.y = y
                self.type = "mario"
                self.w = 60
                self.h = 95
                self.model = model
                self.image_url = "mario1.png"
                super().__init__(x,y,w,h,image_url,model)
                self.imageNum = 0
                self.vert_velocity = 0
                self.numFramesInAir = 0
                self.flip = False
                self.offset = 100
                self.mario_images = []
                self.mario_images.append(pygame.image.load("mario1.png"))
                self.mario_images.append(pygame.image.load("mario2.png"))
                self.mario_images.append(pygame.image.load("mario3.png"))
                self.mario_images.append(pygame.image.load("mario4.png"))
                self.mario_images.append(pygame.image.load("mario5.png"))

        def savePreviousCoordinates(self):
                self.prev_x = self.x
                self.prev_y = self.y

        def updateImage(self):
                self.imageNum = self.imageNum+1
                if self.imageNum > 4:
                        self.imageNum = 0

        def update(self):
                self.image = self.mario_images[self.imageNum]
                
                self.vert_velocity += 3.0
                self.y += self.vert_velocity

                if(self.y < 475 and self.y >= 0):
                        self.numFramesInAir = self.numFramesInAir+1

                if(self.y > 475):
                        self.vert_velocity = 0.0
                        self.y = 475
                        self.numFramesInAir = 0

                if(self.y < 1):
                        self.y = 0
                        if(self.y == 0):
                                self.numFramesInAir = 8
                                self.vert_velocity += 3.7

        def jump(self):
                if(self.numFramesInAir < 8):
                        self.vert_velocity -= 7.0

        def getOutOfSprite(self,s):
                if ((self.x+self.w) >= s.x and (self.prev_x+self.w) <= s.x):
                        self.x = s.x - self.w - 1
                if (self.x <= (s.x+s.w) and self.prev_x >= (s.x+s.w)):
                        self.x = s.x + s.w + 1
                if((self.y+self.h) >= s.y and (self.prev_y+self.h) <= s.y):
                        self.vert_velocity = 0
                        self.numFramesInAir = 0.5
                        self.y = s.y - self.h
                if(self.y <= (s.y+s.h) and self.prev_y >= (s.y+s.h)):
                        self.y = s.y+s.h
                        
class Model():
        def __init__(self):
                self.sprites = []
                self.mario = Mario(200,475,60,95,"mario1.png",self)
                self.sprites.append(self.mario)
                self.tube1 = Tube(400,350,55,400,"tube.png",self)
                self.sprites.append(self.tube1)
                self.tube2 = Tube(750,450,55,400,"tube.png",self)
                self.sprites.append(self.tube2)
                self.tube3 = Tube(1100,375,55,400,"tube.png",self)
                self.sprites.append(self.tube3)
                self.goomba1 = Goomba(550,520,45,54,"goomba.png",self)
                self.sprites.append(self.goomba1)
                self.goomba2 = Goomba(925,520,45,54,"goomba.png",self)
                self.sprites.append(self.goomba2)
                
                self.collide = False
                
        def update(self):

                for sprite in self.sprites:
                        sprite.update()
                        if isinstance(sprite,Goomba):
                                if sprite.dead == True:
                                        sprite.dead = False
                                        pygame.mixer.Sound.play(goomba_dead_sound)
                                        self.sprites.remove(sprite)

                for sprite in self.sprites:
                        index = 0
                        if sprite.type == "tube":
                                for sprite1 in self.sprites:
                                        if sprite1.type == "mario":
                                                self.collision(sprite1,sprite)
                                                if self.collide == True:
                                                        sprite1.getOutOfSprite(sprite)
                                        if sprite1.type == "goomba":
                                                self.collision(sprite1,sprite)
                                                if self.collide == True:
                                                        sprite1.getOutOfSprite(sprite)
                        if sprite.type == "goomba":
                                for sprite1 in self.sprites:
                                        if sprite1.type == "fireball":
                                                self.collision(sprite1,sprite)
                                                if self.collide == True:
                                                        sprite.isOnFire = True
                                                        if sprite.numFramesOnFire < 5:
                                                                pygame.mixer.Sound.play(goomba_fire_sound)
                                                                self.sprites.remove(sprite1)
                        if sprite.type == "fireball":
                                if sprite.x > self.mario.x+775:
                                        self.sprites.remove(sprite)
                                if sprite.x < self.mario.x-200:
                                        self.sprites.remove(sprite)
                                        

        def addFireball(self,x,y):
                self.sprites.append(Fireball(x,y,47,47,"fireball.png",self))
                pygame.mixer.Sound.play(fireball_sound)

        def collision(self,s1,s2):
                if ((s1.x+s1.w) < s2.x):
                        self.collide = False
                elif (s1.x > (s2.x+s2.w)):
                        self.collide = False
                elif ((s1.y+s1.h) < s2.y):
                        self.collide = False
                elif (s1.y > (s2.y+s2.h)):
                        self.collide = False
                else:
                        self.collide = True

class View():
        def __init__(self, model):
                display_width = 800
                display_height = 600
                screen_size = (display_width,display_height)
                self.screen = pygame.display.set_mode(screen_size, 32)
                self.model = model
                self.model.rect = self.model.mario.image.get_rect()
                self.model.rect.center = 200,475

        def update(self):
                self.screen.fill([3,252,244])
                pygame.draw.rect(self.screen,(13,145,22),(0,550,800,50))

                
                for sprite in self.model.sprites:
                        self.screen.blit(pygame.transform.flip(sprite.image,sprite.flip,False),(sprite.x-self.model.mario.x+self.model.mario.offset,sprite.y))
                        
                pygame.display.flip()           

class Controller():
        def __init__(self, model):
                self.model = model
                self.keep_going = True

        def update(self):
                self.model.mario.savePreviousCoordinates()
                
                for event in pygame.event.get():
                        if event.type == QUIT:
                                self.keep_going = False
                        elif event.type == KEYDOWN:
                                if event.key == K_ESCAPE:
                                        self.keep_going = False
                                if event.key == K_LCTRL:
                                        self.fire = False
                                if event.key == K_RCTRL:
                                        self.fire = False
                                        

                        if event.type == KEYUP:
                                if event.key == K_LCTRL:
                                        if(self.model.mario.flip == False):
                                                self.model.addFireball(self.model.mario.x+self.model.mario.w, self.model.mario.y)
                                        elif(self.model.mario.flip == True):
                                                self.model.addFireball(self.model.mario.x, self.model.mario.y)
                                if event.key == K_RCTRL:
                                        if(self.model.mario.flip == False):
                                                self.model.addFireball(self.model.mario.x+self.model.mario.w, self.model.mario.y)
                                        elif(self.model.mario.flip == True):
                                                self.model.addFireball(self.model.mario.x, self.model.mario.y)

                                
                keys = pygame.key.get_pressed()
                if keys[K_LEFT]:
                        self.model.mario.updateImage()
                        self.model.mario.x -= 10
                        self.model.mario.flip = True
                if keys[K_RIGHT]:
                        self.model.mario.updateImage()
                        self.model.mario.x += 10
                        self.model.mario.flip = False
                if keys[K_UP]:
                        if self.model.mario.numFramesInAir < 1:
                                pygame.mixer.Sound.play(jump_sound)
                        self.model.mario.jump()
                elif keys[K_SPACE]:
                        if self.model.mario.numFramesInAir < 1:
                                pygame.mixer.Sound.play(jump_sound)
                        self.model.mario.jump()

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
fireball_sound = pygame.mixer.Sound("smb_fireball.wav")
jump_sound = pygame.mixer.Sound("smb_jump-small.wav")
goomba_dead_sound = pygame.mixer.Sound("smb_bump.wav")
goomba_fire_sound = pygame.mixer.Sound("smb_kick.wav")

m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
        c.update()
        m.update()
        v.update()
        sleep(0.04)
print("Goodbye")
