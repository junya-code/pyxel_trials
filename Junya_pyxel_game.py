import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="junyaゲーム")
        pyxel.run(self.updata, self.draw)

    def updata(self):
        pass

    def draw(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)
        pyxel.text(70, 60, "Start", pyxel.COLOR_YELLOW)


App()
