import sys
from collections import deque


def solve():
    data = sys.stdin.read().split()

    if len(data) < 2:
        return "Impossible"

    M, N = map(int, data[:2])
    cells = ''.join(data[2:])

    if M == 0 or N == 0 or len(cells) != M * N:
        return "Impossible"

    grid = [list(cells[i * N:(i + 1) * N]) for i in range(M)]

    source = [(r, c) for r in range(M) for c in range(N)
              if grid[r][c] == 'l']
    target_cells = [(r, c) for r in range(M) for c in range(N)
                    if grid[r][c] == 'L']

    if not source or len(source) != len(target_cells):
        return "Impossible"

    K = len(source)

    sr, sc = min(r for r, c in source), min(c for r, c in source)
    tr, tc = min(r for r, c in target_cells), min(c for r, c in target_cells)

    so = 0 if len(set(r for r, c in source)) == 1 else 1
    to = 0 if len(set(r for r, c in target_cells)) == 1 else 1

    start = (sr, sc, so)
    target = (tr, tc, to)

    def valid(r, c, o):
        for i in range(K):
            nr = r + (i if o == 1 else 0)
            nc = c + (i if o == 0 else 0)

            if not (0 <= nr < M and 0 <= nc < N):
                return False
            if grid[nr][nc] == 'B':
                return False

        return True

    def free_square(r, c):
        if r < 0 or c < 0 or r + K > M or c + K > N:
            return False

        for i in range(r, r + K):
            for j in range(c, c + K):
                if grid[i][j] == 'B':
                    return False

        return True

    def rotations(r, c, o):
        if o == 0:
            candidates = [
                (r, c, 1),
                (r, c + K - 1, 1),
                (r - K + 1, c, 1),
                (r - K + 1, c + K - 1, 1)
            ]
        else:
            candidates = [
                (r, c, 0),
                (r + K - 1, c, 0),
                (r, c - K + 1, 0),
                (r + K - 1, c - K + 1, 0)
            ]

        for nr, nc, no in candidates:
            if free_square(min(r, nr), min(c, nc)) and valid(nr, nc, no):
                yield (nr, nc, no)

    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        (r, c, o), steps = queue.popleft()

        if (r, c, o) == target:
            return str(steps)

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            state = (nr, nc, o)

            if state not in visited and valid(nr, nc, o):
                visited.add(state)
                queue.append((state, steps + 1))

        for state in rotations(r, c, o):
            if state not in visited:
                visited.add(state)
                queue.append((state, steps + 1))

    return "Impossible"


sys.stdout.write(solve())