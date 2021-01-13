from collections import deque
import numpy as np
import sys
from pprint import *

readline = sys.stdin.readline
write = sys.stdout.write
flush = sys.stdout.flush

command = deque([])
map = [list("#"*(12))]
map += [list("#" + "."*(10) + "#") for _ in range(10)]
map += [list("#"*(12))]
score = np.full((12, 12), 1 << 5)
score[0, :] = 0
score[:, 0] = 0
score[:, 11] = 0
score[11, :] = 0
down_count = 0
hit_count = 0


def candidate():
    check = score*np.random.rand(12, 12)
    xy = np.argmax(check)  # 1次元配列に直される。
    return xy % 12, xy // 12


def query(x1, x2):
    # クエリ: "shot x1 x2" を出力
    write("shot %d %d\n" % (x1, x2))
    flush()
    # ジャッジから返される値を取得
    return readline().strip()


def bfs(N, G):
    # Hit したときの探索アルゴリズム(幅優先探索)
    # G[v]: 頂点vに隣接する頂点list
    # N: 頂点数
    dist = [-1]*N
    que = deque([0])
    dist[0] = 0
    while que:
        v = que.popleft()
        d = dist[v]
        # 停止条件
        for w in G[v]:
            if dist[w] > -1:
                continue
            dist[w] = d + 1
            que.append(w)


def sonner(x, y, resurlt):
    """
    判定から位置を推測し、scoreを更新
    hitの場合、bfsに切り替え
    """
    score[x, y] = 0
    map[x][y] = resurlt
    pass


def debug_mode(x):
    """
    判定から位置を推測し、scoreを更新
    """
    write("! %s\n" % x)
    flush()
    # 即時終了
    exit(0)


def main():
    while True:
        x, y = candidate()
        if map[x][y] != ".":
            continue

        write("shot %d %d\n" % (x, y))
        resurlt = query(x, y)
        if resurlt == "back":
            debug_mode(resurlt)
        sonner(x, y, resurlt)
        print(score)
        flush()


if __name__ == "__main__":
    main()
