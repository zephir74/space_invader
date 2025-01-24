#!/usr/bin/env python

import sdl2 
import sdl2.ext
import sys

RESOURCES = sdl2.ext.Resources(__file__, "resources") 

world = sdl2.ext.World()

class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)

class MovementSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, componentsets):
        for velocity, sprite in componentsets:
            swidth, sheight = sprite.size
            sprite.x += velocity.vx
            sprite.y += velocity.vy
           
            if (sprite.x < self.minx):
                sprite.x = self.minx

            if (sprite.x + swidth > self.maxx):
                sprite.x = self.maxx - swidth
            print("sprite {},{}".format(sprite.x, sprite.y))
            if (sprite.y < self.miny):
                print("delete sprite")
                del sprite

class Velocity(object):
    def __init__(self, vx=0, vy=0):
        super(Velocity, self).__init__()
        self.vx = vx
        self.vy = vy

class Player(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy

class Shot(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0, vx=0,vy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity(vx, vy)

def run():
    sdl2.ext.init()

    window = sdl2.ext.Window("Space Invader", size=(850, 600)) 
    window.show()

    spriterenderer = SoftwareRenderer(window)
    world.add_system(spriterenderer)

    movement = MovementSystem(0, 0, 850, 600)
    world.add_system(movement)

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    ship = factory.from_image(RESOURCES.get_path("ship.png"))
    player = Player(world, ship, 400, 520)

    running = True
    while running:
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_RIGHT: 
                    player.sprite.x += 10
                elif event.key.keysym.sym == sdl2.SDLK_LEFT: 
                    player.sprite.x -= 10
                elif event.key.keysym.sym  == sdl2.SDLK_SPACE:
                    laser = factory.from_image(RESOURCES.get_path("shot.png"))
                    w_ship, h_ship = player.sprite.size
                    w_shot, h_shot = laser.size
                    shot = Shot(world, laser, player.sprite.x - int(w_shot / 2) + int(w_ship / 2), player.sprite.y)
                    shot.velocity.vy = -2
        world.process()
    return 0

print("Press any key to start")

if __name__ == "__main__": 
    sys.exit(run())
