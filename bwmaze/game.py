import pygame as pg
from pygame.sprite import Sprite
import bwmaze.const as G
import bwmaze.levels as L

pg.init()

pg.display.set_caption('maze')
screen = pg.display.set_mode(G.size)
screen.fill(G.bg_colour)
pg.display.flip()


class Wall(Sprite):
    def __init__(self, x, y, screen):
        Sprite.__init__(self)
        self.image = pg.Surface([G.wall_width, G.wall_width])
        self.image.fill('black')
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.screen = screen

    def collided(self, circle):
        cx, cy = circle.rect.center
        r = circle.radius
        if self.x < cx < self.x + G.wall_width:
            if self.y - r < cy < self.y + G.wall_width + r:
                return True
        if self.y < cy < self.y + G.wall_width:
            if self.x - r < cx < self.x + G.wall_width + r:
                return True
        return False


class Player(Sprite):
    def __init__(self, x, y, start, dimension, screen):
        Sprite.__init__(self)

        self.xcor = x
        self.ycor = y
        self.xv = 0
        self.yv = 0
        self.startx, self.starty = start
        self.screenw, self.screenh = dimension

        self.width = G.wall_width // 2
        self.height = G.wall_width // 2
        self.radius = self.width // 2
        self.rect = pg.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)

        self.screen = screen

    def draw(self):
        pg.draw.circle(self.screen, 'red', self.rect.center, G.wall_width//4)

    def move(self):
        self.xcor += self.xv
        self.rect.x = self.xcor - self.width // 2

        outofbound = self.outofbound(self.startx, self.starty,
                                     self.startx + self.screenw * G.wall_width,
                                     self.starty + self.screenh * G.wall_width)

        for wall in walls.sprites():
            if wall.collided(self) or outofbound:
                self.xcor -= self.xv
                self.rect.x = self.xcor - self.width // 2
                self.xv = -self.xv
                print("collided")
                break

        self.ycor += self.yv
        self.rect.y = self.ycor - self.height // 2

        outofbound = self.outofbound(self.startx, self.starty,
                                     self.startx + self.screenw * G.wall_width,
                                     self.starty + self.screenh * G.wall_width)
        for wall in walls.sprites():
            if wall.collided(self) or outofbound:
                self.ycor -= self.yv
                self.rect.y = self.ycor - self.height // 2
                self.yv = -self.yv
                break

        self.xv *= 0.95
        self.yv *= 0.95

        print(self.xv, self.rect.x)

    def outofbound(self, minx, miny, maxx, maxy):
        cx, cy = self.rect.center
        r = self.radius

        return not (
            minx + r < cx < maxx - r and miny + r < cy < maxy - r
        )

    def l(self):
        if self.xv > -6:
            self.xv -= 0.2

    def r(self):
        if self.xv < 6:
            self.xv += 0.2

    def u(self):
        if self.yv > -6:
            self.yv -= 0.2

    def d(self):
        if self.yv < 6:
            self.yv += 0.2


curlevel = L.levels[0]
width, height = curlevel['size']
startx, starty = G.width//2 - width * G.wall_width // 2, G.height//2 - height * G.wall_width // 2
background = pg.Surface([width * G.wall_width, height * G.wall_width])
background.fill("white")
screen.blit(background, (startx, starty, width * G.wall_width, height * G.wall_width))
walls = pg.sprite.Group()

for i in range(height):
    for j in range(width):
        if curlevel['layout'][i][j] == '1':
            newwall = Wall(startx + j * G.wall_width, starty + i * G.wall_width, screen)
            walls.add(newwall)

clock = pg.time.Clock()
p = Player(startx + G.wall_width//2, starty + G.wall_width//2, (startx, starty), curlevel['size'], screen)

def run():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        keydown = pg.key.get_pressed()
        if keydown[pg.K_RIGHT]:
            p.r()
        elif keydown[pg.K_LEFT]:
            p.l()
        elif keydown[pg.K_UP]:
            p.u()
        elif keydown[pg.K_DOWN]:
            p.d()

        screen.blit(background, (startx, starty, width * G.wall_width, height * G.wall_width))
        walls.draw(screen)
        p.move()
        p.draw()

        pg.display.flip()
        clock.tick(G.tick_rate)

run()