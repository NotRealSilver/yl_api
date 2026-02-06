import os
import arcade
from modules import *
from PIL import Image

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 450
WINDOW_TITLE = "MAP"
MAP_FILE = "map.png"


class GameView(arcade.Window):
    def setup(self):
        self.get_image()

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            self.rect
        )

    def get_image(self):
        im = static_maps(ll='60.109599,55.050432', z=12)
        imdata = arcade.texture.ImageData(Image.open(im).convert('RGBA'))
        self.background = arcade.Texture(imdata)


def main():
    gameview = GameView(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    gameview.setup()
    arcade.run()
    os.remove(MAP_FILE)


if __name__ == "__main__":
    main()
