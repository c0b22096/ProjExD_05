import sys
import pygame as pg
import time

WIDTH = 1024
HEIGHT = 1024

class Player(pg.sprite.Sprite):
    move_dict = {
        pg.K_LEFT: (-1, 0),
        pg.K_a: (-1, 0),
        pg.K_RIGHT: (1, 0),
        pg.K_d: (1, 0),
        pg.K_UP: (0, -1),
        pg.K_SPACE: (0, -1)
    }

    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pg.Surface((64, 64))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.gravity_vel = 5
        self.jump_power = 256
        self.isGround = False
        self.state = "normal" # プレイヤーの状態
        self.hyper_life = 0 # 残りの無敵状態時間

    def change_state(self, state: str, hyper_life: int):
        """
        右シフトキーが押された時に, プレイヤーを無敵状態にする関数
        引数1 state : プレイヤーの状態
        引数2 hyper_life : 無敵状態になっている時間
        戻り値 : なし
        """
        self.state = state
        self.hyper_life = hyper_life

    def check_hyper(self):
        """
        プレイヤーが無敵状態かどうかを判定し, プレイヤーの色を変える
        戻り値 : なし
        """
        if self.state == "hyper":
            # プレイヤーが無敵状態だったら
            self.image.fill((168, 88, 168)) # プレイヤーの色を紫にする
            self.hyper_life += -1 # 残りの無敵状態時間を1秒減らす

        if self.hyper_life < 0: # 残りの無敵状態時間が0秒だったら
            self.state == "normal" # プレイヤーを通常状態にする
            self.image.fill((255, 255, 255)) # プレイヤーの色を元に戻す

    def update(self, key_lst: dict):
        for d in __class__.move_dict:
            if key_lst[d]:
                self.rect.x += self.move_dict[d][0] * 3
                if self.isGround:
                    self.rect.y += self.move_dict[d][1] * self.jump_power
                    if self.move_dict[d][1] < 0:
                        self.isGround = False

        if not self.isGround:
            self.rect.y += self.gravity_vel

        self.check_hyper()

class Block(pg.sprite.Sprite):
    size = (32, 32)

    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pg.Surface((32, 32))
        self.image.fill((127, 127, 127))
        self.rect = self.image.get_rect()
        self.rect.center = pos

class Enemy(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((64, 64))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

def main():
    pg.display.set_caption("proto")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.Surface((WIDTH, HEIGHT))
    bg_img.fill((0, 0, 0))

    all_rect_lst = []
    x = 0

    player = Player((500, HEIGHT - 50))
    all_rect_lst.append(player.rect)
    blocks = pg.sprite.Group()
    enemys = pg.sprite.Group()
    enemys.add(Enemy((800, 975)))
    for i in range(256):
        blocks.add(Block((i * Block.size[0], HEIGHT)))
    for i in range(10):
        blocks.add(Block((WIDTH // 2, WIDTH - i * Block.size[1])))
    for b in blocks:
        all_rect_lst.append(b.rect)

    tmr = 0
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            
            if event.type == pg.KEYDOWN and event.key == pg.K_RSHIFT:
                # 右シフトキーが押されたら
                player.change_state("hyper", 400)
        
        key_lst = pg.key.get_pressed()

        player.update(key_lst)

        player.isGround = False
        collide_lst = pg.sprite.spritecollide(player, blocks, False)
        if len(collide_lst) > 0:
            for b in collide_lst:
                if player.rect.top < b.rect.bottom:
                    player.rect.top = b.rect.bottom
                if player.rect.bottom > b.rect.top:
                    player.rect.bottom = b.rect.top
                    player.isGround = True

        for enemy in pg.sprite.spritecollide(player, enemys, True):
            if player.state == "hyper":
                x = 1
            else:
                time.sleep()
                return

        screen.blit(bg_img, (0, 0))
        blocks.draw(screen)
        enemys.draw(screen)
        screen.blit(player.image, player.rect)
        pg.display.update()

        tmr += 1
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
    