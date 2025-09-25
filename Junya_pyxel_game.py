import pyxel


class App:
    def __init__(self):
        pyxel.init(256, 256, title="junyaゲーム")

        pyxel.load("unti.pyxres")

        pyxel.run(self.updata, self.draw)

    def updata(self):
        pass

    def draw(self):
        pyxel.blt(0, 0, 0, 0, 0, 256, 256, 0)
        pyxel.text(20, 60, "Start", pyxel.COLOR_YELLOW)


App()
