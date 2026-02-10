import arcade
from arcade import gui

from modules import *
from PIL import Image

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 550
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
        self.theme = 'light'
        self.pt = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.hor_layout = arcade.gui.UIBoxLayout(vertical=False, space_between=5)
        self.vert_layout = arcade.gui.UIBoxLayout(x=20, y=470, width=500, height=50, vertical=True, space_between=20, align="left")

        self.on_texture = arcade.load_texture(
            ":resources:gui_basic_assets/simple_checkbox/circle_on.png"
        )
        self.off_texture = arcade.load_texture(
            ":resources:gui_basic_assets/simple_checkbox/circle_off.png"
        )
        toggle_label = arcade.gui.UILabel(text='Темная тема', text_color=arcade.color.WHITE, font_size=14)
        toggle = arcade.gui.UITextureToggle(on_texture=self.on_texture, off_texture=self.off_texture, width=20,
                                            height=20)
        toggle.on_change = self.change_theme

        search_label = arcade.gui.UILabel(text='Поиск', text_color=arcade.color.WHITE, font_size=14)
        self.search_field = arcade.gui.UIInputText(width=100, height=22, text_color=arcade.color.WHITE)
        search_btn = arcade.gui.UIFlatButton(text='Искать', width=55, height=20)
        search_btn.on_click = self.on_search

        clear_btn = arcade.gui.UIFlatButton(text='Очистить', width=75, height=20)
        clear_btn.on_click = self.clear_search

        self.address_label = arcade.gui.UILabel(text='Адрес', text_color=arcade.color.WHITE, font_size=14)

        self.hor_layout.add(toggle_label)
        self.hor_layout.add(toggle)
        self.hor_layout.add(search_label)
        self.hor_layout.add(self.search_field)
        self.hor_layout.add(search_btn)
        self.hor_layout.add(clear_btn)
        self.vert_layout.add(self.hor_layout)
        self.vert_layout.add(self.address_label)
        self.manager.add(self.vert_layout)
        self.get_image()

    def clear_search(self, event):
        self.pt = None
        self.address_label.text = ''
        self.get_image()

    def on_search(self, event):
        text = self.search_field.text
        if not text:
            return
        self.lon, self.lat = get_geoobject_coord(geocode(text))
        self.pt = f'{self.lon},{self.lat},flag'
        address = get_address_geoobject(geocode(text))
        self.address_label.text = address
        self.get_image()

    def change_theme(self, val):
        self.theme = 'dark' if val.new_value else 'light'
        self.get_image()

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.rect.LBWH(0, 0, 600, 450)
        )
        self.manager.draw()

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
        params = dict(ll=f'{self.lon},{self.lat}', z=self.zoom, theme=self.theme)
        if self.pt:
            params['pt'] = self.pt
        im = static_maps(**params)
        imdata = arcade.texture.ImageData(Image.open(im).convert('RGBA'))
        self.background = arcade.Texture(imdata)


def main():
    gameview = MapView()
    arcade.run()


if __name__ == "__main__":
    main()
