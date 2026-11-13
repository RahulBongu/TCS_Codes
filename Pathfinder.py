import sys
import heapq


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    it = iter(data)
    n = next(it)
    m = next(it)

    grid = [[next(it) for _ in range(m)] for _ in range(n)]

    sr, sc = next(it) - 1, next(it) - 1
    dr, dc = next(it) - 1, next(it) - 1

    k = next(it)
    blocked = {(next(it) - 1, next(it) - 1) for _ in range(k)}

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),            (0, 1),
        (1, -1),  (1, 0),   (1, 1)
    ]

    neighbors = {}

    for r in range(n):
        for c in range(m):
            if (r, c) in blocked:
                continue

            cells = []
            for dx, dy in directions:
                nr, nc = r + dx, c + dy
                if (0 <= nr < n and 0 <= nc < m
                        and (nr, nc) not in blocked):
                    cells.append((nr, nc))

            neighbors[(r, c)] = cells

    inf = float("inf")
    dist = [[inf] * m for _ in range(n)]
    dist[sr][sc] = 0
    pq = [(0, sr, sc)]

    while pq:
        cost, r, c = heapq.heappop(pq)

        if cost != dist[r][c]:
            continue

        if (r, c) == (dr, dc):
            sys.stdout.write(str(cost))
            return

        adjacent = neighbors[(r, c)]
        current_value = grid[r][c]

        for nr, nc in adjacent:
            highest_other = current_value

            for ar, ac in adjacent:
                if (ar, ac) != (nr, nc):
                    highest_other = max(highest_other, grid[ar][ac])

            addition = max(0, highest_other - grid[nr][nc] + 1)
            new_cost = cost + addition

            if new_cost < dist[nr][nc]:
                dist[nr][nc] = new_cost
                heapq.heappush(pq, (new_cost, nr, nc))

    sys.stdout.write("-1")


if __name__ == "__main__":
    solve()