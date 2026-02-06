import os
import arcade
from modules import *
from PIL import Image

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 450
WINDOW_TITLE = "Часть 2"
KEY_SET = {
    arcade.key.PAGEUP,
    arcade.key.PAGEDOWN,
    arcade.key.LEFT,
    arcade.key.RIGHT,
    arcade.key.UP,
    arcade.key.DOWN,
}


class MapView(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.zoom = 12

    def setup(self):
        self.get_image()

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            self.rect
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.PAGEUP and self.zoom <= 24:
            self.zoom += 1
        elif symbol == arcade.key.PAGEDOWN and self.zoom >= 0:
            self.zoom -= 1

        if symbol in KEY_SET:
            self.get_image()


    def get_image(self):
        im = static_maps(ll='60.109599,55.050432', z=self.zoom)
        imdata = arcade.texture.ImageData(Image.open(im).convert('RGBA'))
        self.background = arcade.Texture(imdata)


def main():
    gameview = MapView()
    gameview.setup()
    arcade.run()


if __name__ == "__main__":
    main()
