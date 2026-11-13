import sys


def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    n, m = int(data[0]), int(data[1])
    chars = ''.join(data[2:])
    grid = [
        list(chars[i * m:(i + 1) * m])
        for i in range(n)
    ]

    # Identify rods that span a complete row or column.
    horizontal_rods = [
        r for r in range(n)
        if all(grid[r][c] != '.' for c in range(m))
        and grid[r].count('R') > grid[r].count('C')
    ]

    vertical_rods = [
        c for c in range(m)
        if all(grid[r][c] != '.' for r in range(n))
        and sum(grid[r][c] == 'R' for r in range(n))
            > sum(grid[r][c] == 'C' for r in range(n))
    ]

    # H means the cable crosses a vertical rod.
    # V means the cable crosses a horizontal rod.
    crossings = {}

    for c in vertical_rods:
        for r in range(n):
            if grid[r][c] == 'C':
                crossings[(r, c)] = 'H'
            elif (
                0 < c < m - 1
                and grid[r][c] == 'R'
                and grid[r][c - 1] == 'C'
                and grid[r][c + 1] == 'C'
            ):
                crossings[(r, c)] = 'H'

    for r in horizontal_rods:
        for c in range(m):
            if grid[r][c] == 'C':
                crossings[(r, c)] = 'V'
            elif (
                0 < r < n - 1
                and grid[r][c] == 'R'
                and grid[r - 1][c] == 'C'
                and grid[r + 1][c] == 'C'
            ):
                crossings[(r, c)] = 'V'

    # Include ordinary cable cells and crossings where
    # the rod is above the cable.
    cable = {
        (r, c)
        for r in range(n)
        for c in range(m)
        if grid[r][c] == 'C'
    }

    for p in crossings:
        r, c = p
        if grid[r][c] == 'R':
            cable.add(p)

    # Build the cable graph without connecting along a rod.
    def can_connect(p, q):
        r, c = p
        nr, nc = q

        if p in crossings:
            if crossings[p] == 'H' and r != nr:
                return False
            if crossings[p] == 'V' and c != nc:
                return False

        if q in crossings:
            if crossings[q] == 'H' and r != nr:
                return False
            if crossings[q] == 'V' and c != nc:
                return False

        return True

    adj = {p: [] for p in cable}

    for r, c in cable:
        for q in ((r + 1, c), (r, c + 1)):
            if q in cable and can_connect((r, c), q):
                adj[(r, c)].append(q)
                adj[q].append((r, c))

    horizontal_sum = {r: 0 for r in horizontal_rods}
    vertical_sum = {c: 0 for c in vertical_rods}
    visited = set()

    # Traverse each cable component.
    for seed in sorted(cable):
        if seed in visited:
            continue

        component = []
        stack = [seed]
        visited.add(seed)

        while stack:
            p = stack.pop()
            component.append(p)

            for q in adj[p]:
                if q not in visited:
                    visited.add(q)
                    stack.append(q)

        endpoints = sorted(
            p for p in component if len(adj[p]) == 1
        )

        current = endpoints[0] if endpoints else component[0]
        previous = None
        path_seen = set()

        while current not in path_seen:
            path_seen.add(current)
            r, c = current

            if current in crossings and previous is not None:
                pr, pc = previous
                sign = 1 if grid[r][c] == 'C' else -1

                if crossings[current] == 'H':
                    direction = 1 if pc < c else -1
                    vertical_sum[c] += direction * sign
                else:
                    direction = 1 if pr < r else -1
                    horizontal_sum[r] += direction * sign

            next_cells = [
                q for q in adj[current]
                if q != previous and q not in path_seen
            ]

            if not next_cells:
                break

            previous, current = current, next_cells[0]

    answer = sum(abs(x) // 2 for x in horizontal_sum.values())
    answer += sum(abs(x) // 2 for x in vertical_sum.values())

    sys.stdout.write(str(answer))


if __name__ == "__main__":
    solve()