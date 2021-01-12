from collections import deque
import numpy as np
import sys

readline = sys.stdin.readline
write = sys.stdout.write
flush = sys.stdout.flush

command = []
map = ["#"*(12)]
map += ["#" + "."*(10) + "#" for _ in range(10)]
map += ["#"*(12)]
score = np.full((12, 12), 1 << 10)


# クエリ: "? x1 x2" を出力
np.random()


def query(x1, x2):
    write(" %d %d\n" % (x1, x2))
    flush()
    # ジャッジから返される値を取得
    return readline().strip()

# 回答: "! x" を出力


def answer(x):
    write("! %d\n" % x)
    flush()
    # 即時終了
    exit(0)


def bfs(N, G):
    # G[v]: 頂点vに隣接する頂点list
    # N: 頂点数
    dist = [-1]*N
    que = deque([0])
    dist[0] = 0
    while que:
        v = que.popleft()
        d = dist[v]
        # 停止条件
        if:
            return
        for w in G[v]:
            if dist[w] > -1:
                continue
            dist[w] = d + 1
            que.append(w)


def main():
    for i in range(1, 100+1):
        print("# %d times" % (i))


main()
