import pygame
from pygame.locals import *


# type Camera struct {
#     state Rect
# }

# func (c *Camera) Apply(Rect Rect) (int, int){
#     return Rect.x + c.state.x, Rect.y + c.state.y
# }

# func (c *Camera) Update(target Rect, w int, h int) {
#     l, t, _, _ := target.Rectangle()
#     bl, bt, wc, hc := c.state.Rectangle()
#     l, t = -l+w/2, -t+h/2

#     l = int(math.Min(0, float64(l)))
#     l = int(math.Max(-float64(c.state.w-w), float64(l)))
#     t = int(math.Max(-float64(c.state.h-h), float64(t)))
#     t = int(math.Min(0, float64(t)))

#     c.state = Rect{bl+(l-bl)/20, bt+(t-bt)/20, wc, hc}
# }
# 
# 
# class Rect:
#     def __init__(self, x, y, w=32, h=32):
#         self.x = x
#         self.y = y
#         self.w = w
#         self.h = h

    

class Camera(object):
    def __init__(self, camera_func, width, height, ww, wh):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)
        self.WIN_WIDTH, self.WIN_HEIGHT = ww, wh

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self, self.state, target.rect)


def simple_camera(self, camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return pygame.Rect(-l+self.WIN_WIDTH/2, -t+self.WIN_HEIGHT/2, w, h)


def complex_camera(self, camera, target_rect):

    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+(self.WIN_WIDTH/2), -t+(self.WIN_HEIGHT/2), w, h

    l = min(0, l)                      # stop scrolling at the left edge
    l = max(-(camera.width-self.WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-self.WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                      # stop scrolling at the top

    # globals.view_object[0].rect.left, globals.view_object[0].rect.top, _, _ = pygame.Rect(l, t, w, h)
    # globals.view_object[0].rect.left = -globals.view_object[0].rect.left
    # globals.view_object[0].rect.top = -globals.view_object[0].rect.top
    return pygame.Rect(l, t, w, h)
