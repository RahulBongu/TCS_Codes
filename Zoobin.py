import sys
from collections import deque


def normalize(edges):
    return tuple(sorted(
        (min(u, v), max(u, v)) for u, v in edges
    ))


def find_cycles(edges):
    adj = {}

    for u, v in edges:
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)

    cycles = set()

    for start in sorted(adj):
        def dfs(path):
            u = path[-1]

            for v in adj[u]:
                if v == start and len(path) >= 3:
                    if path[1] < path[-1]:
                        cycles.add(tuple(path))
                elif v > start and v not in path:
                    dfs(path + [v])

        dfs([start])

    return cycles


def rotate(edges, cycle, direction):
    k = len(cycle)

    mapping = {
        cycle[i]: cycle[(i + direction) % k]
        for i in range(k)
    }

    return normalize([
        (mapping.get(u, u), mapping.get(v, v))
        for u, v in edges
    ])


def minimum_rotations(start, target):
    if start == target:
        return 0

    queue = deque([start])
    distance = {start: 0}

    while queue:
        state = queue.popleft()
        steps = distance[state]

        for cycle in find_cycles(state):
            for direction in (1, -1):
                nxt = rotate(state, cycle, direction)

                if nxt == target:
                    return steps + 1

                if nxt not in distance:
                    distance[nxt] = steps + 1
                    queue.append(nxt)

    return -1


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))

    if not data:
        return

    pos = 0
    e = data[pos]
    pos += 1

    current = []
    for _ in range(e):
        current.append((data[pos], data[pos + 1]))
        pos += 2

    expected = []
    for _ in range(e):
        expected.append((data[pos], data[pos + 1]))
        pos += 2

    answer = minimum_rotations(
        normalize(current),
        normalize(expected)
    )

    sys.stdout.write(str(answer))


if __name__ == "__main__":
    main()