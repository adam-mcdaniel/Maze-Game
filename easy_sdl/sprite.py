import sys
import time
import pygame
from .setup import *
from .tools import *
from collections import deque

keyDown = lambda event, key: event.type == pygame.KEYDOWN and event.key == key
keyUp = lambda event, key: event.type == pygame.KEYUP and event.key == key
TheScreen = None

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        if isinstance(kwargs["image"], pygame.Surface):
            self.image = kwargs["image"]
        elif type(kwargs["image"]) == str:
            self.image = pygame.image.load(kwargs["image"])

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def getImage(self):
        return self.image

    def setImage(self, image):
        self.image = image

    def draw(self, Surface, camera):
        Surface.blit(self.image, camera.apply(self))

    def update(self, entities):
        pass

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def getX(self): return self.rect.x

    def getY(self): return self.rect.y

    def getPos(self):
        return self.getX(), self.getY()

    def getDistance(self, sprite):
        return ((self.getX() - sprite.getX())**2  +  (self.getY() - sprite.getY())**2)**0.5

    def collide(self, sprite):
        return pygame.sprite.collide_rect(self, sprite)

    def __str__(self):
        return "<Sprite at: x={}, y={}>".format(self.rect.x, self.rect.y)


class Surface:
    def __init__(self, sprites):
        self.display = pygame.display.get_surface()
        self.sprites = sprites

    def blit(self, sprite):
        self.display.blit(sprite.getImage(), sprite.rect)

    def update(self, screen):
        pass

    def show(self):
        list(map(lambda s: self.blit(s), self.sprites))

    def pop(self):
        try:
            self.sprites.pop()
        except:
            pass

    def append(self, sprite):
        self.sprites.append(sprite)

    def remove(self, sprite):
        try:
            self.sprites.remove(sprite)
        except:
            pass


class Gif(object):
    """A class to simplify the act of adding animations to sprites."""
    def __init__(self, frames, fps, loops=-1):
        """
        The argument frames is a list of frames in the correct order;
        fps is the frames per second of the animation;
        loops is the number of times the animation will loop (a value of -1
        will loop indefinitely).
        """
        self.frames = frames
        self.fps = fps
        self.frame = 0
        self.timer = time.time()
        self.loops = loops
        self.loop_count = 0
        self.done = False

    def getFrame(self):
        if time.time()-self.timer > 1/self.fps:
            self.frame += 1
            self.timer = time.time()
            if self.frame >= len(self.frames):
                self.frame = 0

        return self.frames[self.frame]

    def reset(self):
        """Set frame, timer, and loop status back to the initialized state."""
        self.frame = 0
        self.timer = None
        self.loop_count = 0
        self.done = False


class AnimatedSprite(Sprite):
    def __init__(self, x, y, **kwargs):
        image_paths = kwargs["images"]
        if "frequency" in kwargs:
            frequency = kwargs["frequency"]
        else:
            frequency = 1

        self.frame = 0
        self.frames = list(map(lambda i: pygame.image.load(path(i)), image_paths))
        Screen.getScreen().addAction(TimedAction(frequency, self.changeFrame))
        super().__init__(x, y, image=image_paths[0])

    def changeFrame(self, screen):
        self.setImage(self.getFrame())

    def getFrame(self):
        if self.frame == len(self.frames):
            self.frame = 0
        frame = self.frames[self.frame]
        self.frame += 1
        return frame

class Screen:
    def __init__(self, w, h, camera, fs=False):
        global TheScreen
        self.sprites = []
        self.surfaces = []
        self.background = False
        if not fs:
            self.display = pygame.display.set_mode((w, h), #pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
                                                   pygame.DOUBLEBUF | pygame.HWSURFACE)
        else:
            self.display = pygame.display.set_mode((w, h), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)

        self.camera = camera
        self.actions = []

        self.width = w
        self.height = h
        TheScreen = self

    def __len__(self):
        return len(self.sprites)

    def __getitem__(self, i):
        return self.sprites[i]

    def getScreen():
        return TheScreen

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setBackground(self, sprite):
        self.background = sprite

    def append(self, sprite):
        self.sprites.append(sprite)

    def remove(self, sprite):
        try:
            self.sprites.remove(sprite)
        except:
            pass

    def add(self, sprites):
        self.sprites.extend(sprites)

    def addAction(self, action):
        self.actions.append(action)

    def addSurface(self, surface):
        self.surfaces.append(surface)

    def blit(self, sprite, rect):
        try:
            self.display.blit(sprite, rect)
        except:
            print(sprite)

    def fill(self, color):
        self.display.fill(color)

    def focus(self, sprite):
        self.camera.update(sprite)

    def update(self):
        self.fill((0, 0, 0))

        if self.background:
            self.background.draw(self, self.camera)

        for sprite in self.sprites:
            sprite.update(self)
            sprite.draw(self, self.camera)

        list(map(lambda a: a.update(self), self.actions))

        list(map(lambda s: s.update(self), self.surfaces))
        list(map(lambda s: s.show(), self.surfaces))

        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    pygame.mouse.set_visible(False)
    s = Screen(WIN_WIDTH, WIN_HEIGHT)
    # s = Screen(640, 480)
    s.fill((0, 0, 0))
    spr = Boomerang(0,120)
    s.append(spr)
    while True:
        # s.blit(pygame.image.load("/Users/kiwi/Desktop/old-desktop/desktop/py/b4/library/resources/weapon/boomerang1.png"), (0, 0))
        s.update()
        print(s[0])
