import pygame as pg


class Global:
    size = width, height = 520, 520

    speed = [200, 100, 50]
    speed_idx = 1

    spacing = 24
    snake_width = 23
    food_width = 20

    snake_colour = "white"
    food_colour = "gold"
    bg_colour = "black"
    border_colour = "white"

    border_ratio = 0.8
    border_thickness = 2

    tick_rate = 60




def drawBorder(screen):
    width_offset = (1 - Global.border_ratio) * Global.width // 2
    height_offset = (1 - Global.border_ratio) * Global.height // 2

    corners = [
        [width_offset, height_offset],
        [Global.width - width_offset, height_offset],
        [Global.width - width_offset, Global.height - height_offset],
        [width_offset, Global.height - height_offset],
    ]

    for i in range(-1, 3):
        pg.draw.line(screen, Global.border_colour, corners[i], corners[i+1], Global.border_thickness)

    pg.display.flip()


class Food:
    def __init__(self, x, y, screen):
        pg.draw.circle(screen, Global.food_colour, (x,y), Global.food_width//2)
        pg.display.flip()

    def clear(self, screen):
        screen.fill(Global.bg_colour)
        drawBorder(screen)


class Body:
    pass


class Snake:
    pass


class Game:
    def __init__(self, screen):
        self.screen = screen
        print("Game started")

    def exit_game(self):
        print("GG")

    def check_end(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True
        return False

    def run(self):
        clock = pg.time.Clock()

        while True:
            if self.check_end():
                self.exit_game()
                return

            clock.tick(Global.tick_rate)





def main():
    pg.init()

    pg.display.set_caption("snek")
    screen = pg.display.set_mode(Global.size)
    screen.fill(Global.bg_colour)
    drawBorder(screen)


    game = Game(screen)
    game.run()


if __name__=="__main__":
    main()
    pg.quit()
