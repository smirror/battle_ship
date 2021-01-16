from collections import deque
import numpy as np
import sys
from pprint import *
import resource
import random

sys.setrecursionlimit(10**9)
resource.setrlimit(resource.RLIMIT_STACK, (-1, -1))


class battle_ship:
    readline = sys.stdin.readline
    write = sys.stdout.write
    flush = sys.stdout.flush

    def __init__(self, command_map):
        self.command_map = command_map
        self.command = deque([])
        map = [list("#"*(12))]
        map += [list("#" + "."*(10) + "#") for _ in range(10)]
        map += [list("#"*(12))]
        self.map = map

        score = np.zeros((12, 12), dtype=np.int32)
        candidate = []
        prob = 1 << 6
        for i in range(1, 11):
            for j in range(1, 11, 2):
                if i % 2:
                    score[i, j] = prob
                    candidate.append(12*i + j)
                else:
                    score[i, j+1] = prob
                    candidate.append(12*i + (j+1))
        self.score = score
        self.random = deque(random.sample(candidate, k=50))
        self.state = "Random"

        self.downs_count = 0
        self.hits_count = 0
        self.shots_count = 0

    def query(self, x: int, y: int):
        # ユーザーが現在の状態を把握するために、クラス内の重要な変数を出力
        self.write("downs count: %d\n" % self.downs_count)
        self.write("hits count:%d\n" % self.hits_count)
        self.map[x][y] = "@"
        pprint(self.map)
        self.map[x][y] = '.'
        self.flush()
        # pprint(self.score)
        self.write("State: %s\n" % self.state)
        # クエリ: "shot x1 x2" を出力
        self.write("shot %d %d\n" % (x, y))
        self.write(
            "send me result if :/hit -> 'h' / down -> 'd' / miss -> 'm': %s\n" % self.command_map[x-1][y-1])
        self.flush()
        # ジャッジから返される値を取得
        # return self.readline().strip()
        return self.command_map[x-1][y-1]

    def dfs(self, sx: int, sy: int):
        self.state = "DFS"
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = sx+dx, sy+dy
            result = self.check(nx, ny)
            while self.hit(result):
                nx, ny = nx+dx, ny+dy
                result = self.check(nx, ny)

            if result == "h" or result == "d":
                if result == "d":
                    return
                nx, ny = sx-dx, sy-dy
                result = self.check(nx, ny)
                while self.hit(result):
                    nx, ny = nx-dx, ny-dy
                    result = self.check(nx, ny)
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
            if self.hits_count == 17:
                # if self.hits_count == 17 and self.downs_count == 5:
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
            if(self.hits_count <= 14 or self.downs_count <= 3):
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
        xy = self.random.popleft()
        x, y = xy // 12, xy % 12
        if self.map[x][y] != ".":
            return
        result = self.check(x, y)
        self.sonner(x, y, result)


if __name__ == "__main__":
    command_map = [list("mmmmmmmmmm"), list("hhmmmmmmmh"), list("mmhmmmmmmh"), list("mmhmmmmmmh"), list("mmhmmmmmmh"),
                   list("mmhmmmmmmm"), list("hmmmmmmmmm"), list("hmmmmmmmmm"), list("hmmmmmmmmm"), list("hmmmmmhhhh")]
    bs = battle_ship(command_map)
    while True:
        bs.main()
