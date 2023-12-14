import pygame as pg
import sys
from settings import *
from objects import *
from os import path
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        self.font=path.join("ARIAL.TTF")
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        arr = [[-1,1,-1,1],[8,4,2,1],[3,2,1,0],[12,4,1,0]]
        arrId = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

        self.matrix = Matrix(arr, 100, 100,100,self)
        self.matrixId = Matrix(arrId, 100, 550,100,self)
        self.matricies = [self.matrix, self.matrixId]
        self.input = Input(vec(0, HEIGHT - 50),WIDTH,50,self)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        # fps
        self.draw_text(str(int(self.clock.get_fps())), self.font, 40, WHITE, 50, 50, align="center")

        self.matrix.draw(self.screen)
        self.matrixId.draw(self.screen)
        self.input.draw(self.screen)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()



                if event.key == pg.K_LEFT:
                    if len(self.matricies[0].backUps)>1:
                        for m in self.matricies:
                                m.backUps= m.backUps[:-1]
                                m.operations = m.operations[:-1]
                                m.mat = m.backUps[-1]
                                m.updateCells()
                                print(m.backUps)





                if event.key ==pg.K_RETURN:
                    for m in self.matricies:
                        m.execute(self.input.text)
                        m.saveMat()
                        m.updateCells()

                    self.input.text = ""


                elif event.key==pg.K_BACKSPACE and event.key != pg.K_RETURN:
                    self.input.text=self.input.text[:-1]

                else:
                    self.input.text+=event.unicode

                



# create the game object
g = Game()
g.new()
g.run()
