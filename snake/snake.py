import time

import pygame
import pygame as pg
import pygame.sprite
import random as r

import const as G

# Global variables
# class G:

#     spacing = 24
#     snake_width = 22
#     food_width = 22
#
#     border_ratio = 0.8
#     border_thickness = 2
#
#     gridx = 20
#     gridy = 20
#
#     size = width, height = round(gridx * spacing / border_ratio), round(gridy * spacing / border_ratio)
#
#     snake_colour = "white"
#     food_colour = "gold"
#     bg_colour = "black"
#     border_colour = "white"
#     text_colour = "white"
#
#     font_size = 24
#     font_path = None
#
#     tick_rate = 60
#

def drawBorder(screen):
    width_offset = round((1 - G.border_ratio) * G.width / 2 - G.border_thickness - (G.spacing - G.snake_width)/2)
    height_offset = round((1 - G.border_ratio) * G.height / 2 - G.border_thickness - (G.spacing - G.snake_width)/2)

    corners = [
        [width_offset-1, height_offset-1],
        [G.width - width_offset-1, height_offset-1],
        [G.width - width_offset-1, G.height - height_offset-1],
        [width_offset-1, G.height - height_offset-1],
    ]

    for i in range(-1, 3):
        pg.draw.line(screen, G.border_colour, corners[i], corners[i + 1], G.border_thickness)


class Food:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

        self.draw()

    def draw(self):
        pg.draw.circle(self.screen, G.food_colour, (self.x, self.y), G.food_width // 2)

    def clear(self, screen):
        screen.fill(G.bg_colour)
        drawBorder(screen)


class Body(pg.sprite.Sprite):
    def __init__(self, x, y, color=G.snake_colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([G.snake_width, G.snake_width])
        self.image.fill(color)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()


    def update(self):
        self.rect.x = self.x - G.snake_width//2
        self.rect.y = self.y - G.snake_width//2

    def clear(self):
        pass
        #TODO


class Snake:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.font = pg.font.SysFont(G.font_path, G.font_size)

        self.sound = pg.mixer.Sound("./eat.wav")

        self.alive = True
        self.length = 1
        self.direction = "R"

        self.body = []
        self.body.append(Body(x, y))
        self.group = pg.sprite.Group()
        self.group.add(self.body[0])

        width_offset = round((1 - G.border_ratio) * G.width / 2 + G.spacing / 2)
        height_offset = round((1 - G.border_ratio) * G.height / 2 + G.spacing / 2)

        # TODO: right and left limits are swapped
        self.LLimit = width_offset
        self.Ulimit = height_offset
        self.RLimit = self.LLimit + (G.gridx-1) * G.spacing
        self.Dlimit = self.Ulimit + (G.gridy-1) * G.spacing

        # todo: Fix limits

        rx = r.randrange(self.LLimit, self.RLimit, G.spacing)
        ry = r.randrange(self.Ulimit, self.Dlimit, G.spacing)
        self.food = Food(rx, ry, screen)

        self.draw()

    def draw(self):
        self.clear()
        self.food.draw()
        self.group.draw(self.screen)
        score = self.font.render(f"Score: {self.length}", True, G.text_colour)

        self.screen.blit(score, (self.LLimit-G.spacing//2, self.Ulimit - 1.5 * (G.spacing + G.border_thickness)))

    def clear(self):
        self.food.clear(self.screen)
        for b in self.body:
            b.clear()

    def move(self):
        prevx = self.x
        prevy = self.y

        if self.direction == "L":
            if self.x - G.spacing < self.LLimit:
                newx = self.RLimit
            else:
                newx = self.x - G.spacing
            newy = self.y

        if self.direction == "R":
            if self.x + G.spacing > self.RLimit:
                newx = self.LLimit
            else:
                newx = self.x + G.spacing
            newy = self.y

        if self.direction == "U":
            if self.y - G.spacing < self.Ulimit:
                newy = self.Dlimit
            else:
                newy = self.y - G.spacing
            newx = self.x

        if self.direction == "D":
            if self.y + G.spacing > self.Dlimit:
                newy = self.Ulimit
            else:
                newy = self.y + G.spacing
            newx = self.x

        for i in range(self.length - 1):
            if newx == self.body[i].x and newy == self.body[i].y:
                self.alive = False
                self.clear()
                return

        if newx == self.food.x and newy == self.food.y:
            print("Food detected, new length:", self.length + 1)
            pg.mixer.Sound.play(self.sound)
            self.body.append(Body(newx, newy))
            self.group.add(self.body[-1])
            self.length += 1
            rx = r.randrange(self.LLimit, self.RLimit, G.spacing)
            ry = r.randrange(self.Ulimit, self.Dlimit, G.spacing)
            self.food = Food(rx, ry, self.screen)

        self.body[-1].x = newx
        self.body[-1].y = newy
        self.body[-1].update()

        last = self.body.pop(-1)
        self.body.insert(0, last)
        self.x = newx
        self.y = newy

        print(f"x,y: {newx}, {newy}")

        self.draw()

    def l(self):
        if not self.direction == "R":
            self.direction = "L"

    def r(self):
        if not self.direction == "L":
            self.direction = "R"

    def u(self):
        if not self.direction == "D":
            self.direction = "U"

    def d(self):
        if not self.direction == "U":
            self.direction = "D"


class Game:
    def __init__(self, screen):
        self.screen = screen
        print("Game started")

    def exit_game(self):
        print("GG")

    def game_over(self, score):
        msgfont = pg.font.SysFont(G.font_path, G.font_size)
        msg = msgfont.render(f"Game Over, score: {score}, press space to restart", True, G.text_colour)

        self.screen.blit(msg, (G.width//2-msg.get_width()//2, G.height//2))
        pg.display.flip()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit_game()
                    return 0
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        return 1

    def run(self):
        clock = pg.time.Clock()

        # g = pg.sprite.Group()
        # b = Body()
        # g.add(b)
        #
        # g.draw(self.screen)
        # pg.display.flip()

        init_x = round((1 - G.border_ratio) * G.width / 2 + (G.gridx//2) * G.spacing  + G.spacing / 2)
        init_y = round((1 - G.border_ratio) * G.height / 2 + (G.gridy//2) * G.spacing  + G.spacing / 2)
        s = Snake(init_x, init_y, self.screen)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit_game()
                    return
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        s.r()
                    elif event.key == pg.K_LEFT:
                        s.l()
                    elif event.key == pg.K_UP:
                        s.u()
                    elif event.key == pg.K_DOWN:
                        s.d()
            s.move()
            pg.display.flip()

            if not s.alive:
                print("Score:",s.length)
                if (over := self.game_over(s.length)) <= 0:
                    print("Over", over)
                    return
                elif over == 1:
                    init_x = round((1 - G.border_ratio) * G.width / 2 + (G.gridx // 2) * G.spacing + G.spacing / 2)
                    init_y = round((1 - G.border_ratio) * G.height / 2 + (G.gridy // 2) * G.spacing + G.spacing / 2)
                    s = Snake(init_x, init_y, self.screen)
                    print("restarted")

            clock.tick(G.tick_rate)


def main():
    pg.init()

    pg.display.set_caption("lore accurate Python 3")
    screen = pg.display.set_mode(G.size)
    screen.fill(G.bg_colour)
    drawBorder(screen)
    pg.display.flip()

    game = Game(screen)
    game.run()


if __name__ == "__main__":
    main()
    pg.quit()
