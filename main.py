from collections import deque
import numpy as np
import sys


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
        self.score = score

        self.downs_count = 0
        self.hits_count = 0
        self.shots_count = 0

    def candidate(self):
        check = self.score*np.random.rand(12, 12)
        xy = np.argmax(check)  # 1次元配列に直される。
        return xy % 12, xy // 12

    def query(self, x: int, y: int):
        # クエリ: "shot x1 x2" を出力
        self.write("shot %d %d\n" % (x, y))
        self.flush()
        # ジャッジから返される値を取得
        return self.readline().strip()

    def check(self, x: int, y: int):
        # 判定結果からscoreを更新

        self.shots_count += 1
        result = self.query(x, y)
        self.command.append((x, y))
        if result == "back":
            self.debug_mode(result)

        self.write("Counts: %d\n" % self.shots_count)
        self.flush()

        self.score[x, y] = 0
        self.map[x][y] = result

        return result

    def bfs(self, sx: int, sy: int):
        que = deque([(sx, sy)])
        while que:
            x, y = que.popleft()
            # 停止条件
            if self.hits_count == 17:
                return
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx, ny = x+dx, y+dy
                if self.map[nx][ny] != ".":
                    continue
                result = self.check(nx, ny)
                if self.hit(self, result):
                    que.append((nx, ny))

    def hit(self, result):
        # hitしているかの判定
        # TODO: 勝利宣言のメッセージの条件分岐を変える(この場合ではhitが最終状態にはならない)
        # しかし、そもそもDown情報が意味があるかと言われると。。。
        if result == "hit":
            self.hits_count += 1
            if self.hits_count == 17:
                self.write("Conglaturations on Your Win!!")
        elif result == "down":
            self.downs_count += 1
            if self.downs_count == 5:
                self.write("Conglaturations on Your Win!!")

        return result == "hit"

    def sonner(self, x: int, y: int, result: str):
        """
        判定から位置を推測
        hitの場合、dfsに切り替え
        """
        if self.hit(self, result):
            self.bfs(x, y)
        return

    def debug_mode(self, x):
        """
        判定から位置を推測し、scoreを更新
        """
        self.write("! %s\n" % x)
        self.flush()
        # 即時終了
        exit(0)

    def main(self):
        while True:
            if self.shots_count == 100:
                self.write("Input's map is Wrong")
            x, y = self.candidate()
            if self.map[x][y] != ".":
                continue
            result = self.check(x, y)
            self.sonner(x, y, result)


if __name__ == "__main__":
    bs = battle_ship()
    bs.main()
