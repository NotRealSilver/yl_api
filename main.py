import arcade
from modules import *
from PIL import Image

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 450
WINDOW_TITLE = "Часть 3"
KEY_SET = {
    arcade.key.PAGEUP,
    arcade.key.PAGEDOWN,
    arcade.key.LEFT,
    arcade.key.RIGHT,
    arcade.key.UP,
    arcade.key.DOWN,
}
DELTA_X = 180
DELTA_Y = 120


class MapView(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.zoom = 10
        self.lon = 60.109599
        self.lat = 55.050432
        self.get_image()

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            self.rect
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.PAGEUP and self.zoom <= 21:
            self.zoom += 1
        elif symbol == arcade.key.PAGEDOWN and self.zoom >= 0:
            self.zoom -= 1

        if symbol == arcade.key.LEFT:
            self.lon = (self.lon + 180 - DELTA_X / (2 ** self.zoom)) % 360 - 180
        elif symbol == arcade.key.RIGHT:
            self.lon = (self.lon + 180 + DELTA_X / (2 ** self.zoom)) % 360 - 180
        elif symbol == arcade.key.UP:
            self.lat = min(85, self.lat + DELTA_Y / (2 ** self.zoom))
        elif symbol == arcade.key.DOWN:
            self.lat = max(-85, self.lat - DELTA_Y / (2 ** self.zoom))

        if symbol in KEY_SET:
            self.get_image()


    def get_image(self):
        im = static_maps(ll=f'{self.lon},{self.lat}', z=self.zoom)
        imdata = arcade.texture.ImageData(Image.open(im).convert('RGBA'))
        self.background = arcade.Texture(imdata)


def main():
    gameview = MapView()
    arcade.run()


if __name__ == "__main__":
    main()
