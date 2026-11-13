import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))
    names = [next(it) for _ in range(n)]
    skills = [int(next(it)) for _ in range(n)]
    ids = {name: i for i, name in enumerate(names)}

    n1 = int(next(it))
    partner = [-1] * n

    for _ in range(n1):
        a = ids[next(it)]
        b = ids[next(it)]
        partner[a] = b
        partner[b] = a

    n2 = int(next(it))
    rivals = []

    for _ in range(n2):
        a = ids[next(it)]
        b = ids[next(it)]
        rivals.append((a, b))

    limit = int(next(it))

    group_of = [-1] * n
    weights = []
    counts = []

    for i in range(n):
        if group_of[i] != -1:
            continue

        members = [i]
        if partner[i] != -1:
            members.append(partner[i])

        gid = len(weights)

        for p in members:
            group_of[p] = gid

        weights.append(sum(skills[p] for p in members))
        counts.append(len(members))

    forbidden = set()
    edges = set()

    for a, b in rivals:
        x = group_of[a]
        y = group_of[b]

        if x == y:
            forbidden.add(x)
        else:
            edges.add((min(x, y), max(x, y)))

    for i, w in enumerate(weights):
        if w > limit:
            forbidden.add(i)

    edges = {
        (x, y) for x, y in edges
        if x not in forbidden and y not in forbidden
    }

    active_set = set()
    for x, y in edges:
        active_set.add(x)
        active_set.add(y)

    active = sorted(active_set)
    free = [
        i for i in range(len(weights))
        if i not in forbidden and i not in active_set
    ]

    dp = [0] * (limit + 1)

    for i in free:
        w = weights[i]
        c = counts[i]

        for cap in range(limit, w - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - w] + c)

    m = len(active)
    index = {gid: i for i, gid in enumerate(active)}
    adj = [0] * m

    for x, y in edges:
        a = index[x]
        b = index[y]
        adj[a] |= 1 << b
        adj[b] |= 1 << a

    answer = dp[limit]

    def dfs(pos, mask, score, people):
        nonlocal answer

        if pos == m:
            answer = max(
                answer,
                people + dp[limit - score]
            )
            return

        dfs(pos + 1, mask, score, people)

        gid = active[pos]
        w = weights[gid]

        if score + w <= limit and not (adj[pos] & mask):
            dfs(
                pos + 1,
                mask | (1 << pos),
                score + w,
                people + counts[gid]
            )

    dfs(0, 0, 0, 0)
    sys.stdout.write(str(answer))


if __name__ == "__main__":
    solve()