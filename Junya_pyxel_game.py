import pyxel


class Enemy:
    NUM_STARS = 100

    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.stars = []  # 星の座標と速度のリスト

        # 星の座標と速度を初期化してリストに登録する
        for i in range(Enemy.NUM_STARS):
            x = pyxel.rndi(0, pyxel.width - 1)  # X座標
            y = pyxel.rndi(0, pyxel.height - 1)  # Y座標
            vy = pyxel.rndf(1, 2.5)  # Y方向の速度
            self.stars.append((x, y, vy))  # タプルとしてリストに登録

        # ゲームに背景を登録する

    # 背景を更新する
    def update(self):
        for i, (x, y, vy) in enumerate(self.stars):
            y += vy
            if y >= pyxel.height:  # 画面下から出たか
                y -= pyxel.height  # 画面上に戻す
            self.stars[i] = (x, y, vy)

    # 背景を描画する
    def draw(self):

        # 星を描画する
        for x, y, speed in self.stars:
            color = 6  # 速度に応じて色を変える
            pyxel.pset(x, y, color)


class Player:
    def __init__(self, x, y):

        self.x = x
        self.y = y

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 4
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 4
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 4
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 4

        # 画面外に出ないように制限（8x8サイズ前提）
        self.x = max(0, min(self.x, pyxel.width - 8))
        self.y = max(0, min(self.y, pyxel.height - 8))


class App:
    def __init__(self):
        pyxel.init(160, 120, title="junyaゲーム")

        pyxel.load("unti.pyxres")
        self.init_sound()
        self.music = False
        self.player = Player(72, 85)
        self.score = Enemy.NUM_STARS
        self.Enemy = Enemy(40, 40, self.score)

        pyxel.playm(1, loop=True)
        pyxel.run(self.update, self.draw)

    def init_sound(self):
        # Set sound effects
        pyxel.sounds[0].set("a3a2c1a1", "p", "7", "s", 5)
        pyxel.sounds[1].set("a3a2c2c2", "n", "7742", "s", 10)

        # Set title music
        a1 = "T128 Q96 @2 @ENV1{127,6,96} O4 L16 @VIB1{36,18,25} K-2"
        a2 = "D8.C8.D4G8AB->CD C8.<F2R FFGA B-8.A8.B-4.GGAB-"
        a3 = "RR>CC<B->C8 D8.D8CD8.<"

        b1 = "T128 Q90 @0 V96 O3 L16"
        b2 = "FFR4 FFR4 <F4> E-E-R4 E-E-R4 <E-4> D-D-R4 D-D-R4 <D-4> E-E-R4 E-E-R4 EEE8"

        c1 = "T128 Q50 @3 L16 @ENV1{48,8,0} @ENV2{127,6,0}"
        c2 = "[@ENV1 O7 FFR4 FFR4 @ENV2 O3 G4]3 @ENV1 O7 FFR4 FFR4 FF @ENV2 O3 G8"

        pyxel.sounds[2].mml(a1 + a2 + a3)
        pyxel.sounds[3].mml(b1 + b2)
        pyxel.sounds[4].mml(c1 + c2)
        pyxel.musics[0].set([2], [3], [4])

        # Set play music
        a1 = "T150 Q96 @1 @ENV1{127,12,64} O4 L16"
        a4 = "RR>CC<B->C8 D8.D8C<A8G&1"

        b1 = "T150 Q96 @1 @ENV1{112,12,56} @ENV2{64,8,0} O4 L16 @ENV1 "
        b2 = "<B-8.A8.B-4>D8DDGB- A8.<A2R AA>CF G8.F8.G4.E-E-FG"
        b3 = "RRAAGA8 A8.A8GA8."
        b4 = "RRAAGA8 A8.A8GD8 Q100 C&4.<B4. @3 O7 @ENV2 FFFF"

        c1 = "T150 Q100 @0 V96 O3 L16 @GLI1{400,4} @GLI0 "
        c2 = "[<G.R32>DG]4 [<F.R32>CF]4 [<E-.R32B->E-]4"
        c3 = "Q80 <F8FF>F<F8 F+8RF+8>F+<F+8.>"
        c4 = "Q80 @GLI0 <F8FF>F<F8F+8RF+8>F+<F+8 Q100 G8R>DG<[G.R32>DG<]2 @GLI1 Q50 >>CC<F8>"

        pyxel.sounds[5].mml(a1 + a2 + a3 + a2 + a4)
        pyxel.sounds[6].mml(b1 + b2 + b3 + b2 + b4)
        pyxel.sounds[7].mml(c1 + c2 + c3 + c2 + c4)
        pyxel.musics[1].set([5], [6], [7])

        # You can also use 8bit BGM generator for music:
        #   load_bgm(0, "assets/bgm_title.json", 2, 3, 4)
        #   load_bgm(1, "assets/bgm_play.json", 5, 6, 7)

    def check_collision(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return x1 < x2 + w2 and x2 < x1 + w1 and y1 < y2 + h2 and y2 < y1 + h1

    def update(self):
        self.player.update()
        self.Enemy.update()

        self.hit = False
        # 当たり判定（プレイヤーと星）
        new_stars = []

        for x, y, vy in self.Enemy.stars:
            if self.check_collision(self.player.x, self.player.y, 8, 8, x, y, 1, 1):
                self.hit = True
                self.score -= 1
                pyxel.play(3, 0)
            else:
                new_stars.append((x, y, vy))  # 当たってない星だけ残す
        self.Enemy.stars = new_stars

        if self.score == 0 and not self.music:
            pyxel.stop()
            pyxel.playm(0, loop=True)
            self.music = True

    def draw(self):
        pyxel.blt(0, 0, 0, 0, 0, 160, 120, 0)
        pyxel.blt(self.player.x, self.player.y, 1, 0, 0, 8, 8, 1)
        self.Enemy.draw()
        if self.hit:
            pyxel.text(
                pyxel.width / 2 - 10, 30, f"{self.score}", pyxel.frame_count % 16
            )  # 点滅する色で表示
        elif self.score > 0:
            pyxel.text(pyxel.width / 2 - 10, 30, f"{self.score}", 0)

        if self.score == 0:
            pyxel.text(45, 30, "Tokumaru Junya", pyxel.frame_count % 16)


App()
