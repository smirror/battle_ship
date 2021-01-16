from itertools import product
from collections import deque
import numpy as np
import sys
from pprint import *


class battle_ship:
    readline = sys.stdin.readline
    write = sys.stdout.write
    flush = sys.stdout.flush

    def __init__(self):
        self.command = deque([])
        map = [list("#"*(12))]
        map += [list("#" + "."*(10) + "#") for _ in range(10)]
        map += [list("#"*(12))]
        self.map = map

        score = np.full((12, 12), 1 << 5)
        score[0, :] = 0
        score[:, 0] = 0
        score[:, 11] = 0
        score[11, :] = 0
        for i in range(1, 11):
            for j in range(1, 11, 2):
                if i % 2:
                    score[i, j] = 0
                else:
                    score[i, j+1] = 0

        self.score = score

        self.state = "Random"

        self.downs_count = 0
        self.hits_count = 0
        self.shots_count = 0

    def random_choice(self):
        check = self.score*np.random.rand(12, 12)
        xy = np.argmax(check)  # 1次元配列に直される。
        return xy % 12, xy // 12

    def query(self, x: int, y: int):
        # ユーザーが現在の状態を把握するために、クラス内の重要な変数を出力
        self.write("downs count: %d\n" % self.downs_count)
        self.write("hits count:%d\n" % self.hits_count)
        self.map[x][y] = "@"
        pprint(self.map)
        self.map[x][y] = '.'
        # pprint(self.score)
        self.write("State: %s\n" % self.state)
        # クエリ: "shot x1 x2" を出力
        self.write("shot %d %d\n" % (x, y))
        self.write(
            "send me result if :/hit -> 'h' / down -> 'd' / miss -> 'm': ")
        self.flush()
        # ジャッジから返される値を取得
        return self.readline().strip()

    def dfs(self, sx: int, sy: int):
        self.state = "DFS"
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = sx+dx, sy+dy
            result = self.check(nx, ny)
            while self.hit(result):
                nx, ny = nx+dx, ny+dy
                result = self.check(nx, ny)
            if result == "d":
                return

    def bfs(self, sx: int, sy: int):
        self.state = "BFS"
        que = deque([(sx, sy)])
        candidate = []
        while que:
            x, y = que.popleft()
            # 停止条件
            if self.hits_count == 17:
                return
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx, ny = x+dx, y+dy
                if self.map[nx][ny] == ".":
                    candidate.append((nx, ny))
                elif self.map[nx][ny] == "h":
                    que.append((nx, ny))
        return candidate

    def check(self, x: int, y: int):
        # 判定結果からscoreを更新
        if self.map[x][y] != ".":
            return 'c'  # shotしては行けない場所を指し示しているため、位置を変更

        self.shots_count += 1
        result = self.query(x, y)
        if result == "back":
            self.debug_mode(result)
        self.command.append((x, y))

        self.write("Counts: %d\n" % self.shots_count)
        self.flush()

        self.score[x, y] = 0
        self.map[x][y] = result

        return result

    def hit(self, result):
        # hitしているかの判定
        if result == "h" or result == "d":
            if result == "d":
                self.downs_count += 1
            self.hits_count += 1
            if self.hits_count == 17 and self.downs_count == 5:
                self.write("Conglaturations on Your Win!!\n")
                pprint(self.map)
                exit(0)

        return result == "h"

    def sonner(self, x: int, y: int, result: str):
        """
        判定から位置を推測
        hitの場合、dfsに切り替え
        """
        if self.hit(result):
            if(self.hits_count < 14 or self.downs_count <= 3):
                self.dfs(x, y)
            else:
                candidate = self.bfs(x, y)
                for nx, ny in candidate:
                    count = 0
                    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                        if self.map[nx+dx][ny+dy] == "h":
                            count += 1
                    if count >= 2:
                        result = self.check(nx, ny)
                        self.hit(result)
        self.state = "Random"
        return

    def debug_mode(self, x):
        """
        コマンドの巻き戻しやselfの変数を確認するモード
        現在は終了コマンド
        """
        self.write("! %s\n" % x)
        self.flush()
        # 即時終了
        exit(0)

    def main(self):
        if self.shots_count == 100:
            self.write("Input's map is Wrong")
        x, y = self.random_choice()
        if self.map[x][y] != ".":
            return
        result = self.check(x, y)
        self.sonner(x, y, result)


if __name__ == "__main__":
    bs = battle_ship()
    print(bs.score)
    while True:
        bs.main()
