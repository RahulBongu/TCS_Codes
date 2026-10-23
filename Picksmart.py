import math
import sys

def segment_intersection(p1, p2, p3, p4):
    """
    Finds the intersection point of segment p1-p2 and p3-p4.
    Returns (x, y) rounded to 2 decimal places if they intersect, else None.
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    dx1, dy1 = x2 - x1, y2 - y1
    dx2, dy2 = x4 - x3, y4 - y3

    denom = dx1 * dy2 - dy1 * dx2
    if denom == 0:
        return None  # Parallel or collinear

    num_t = (x3 - x1) * dy2 - (y3 - y1) * dx2
    num_u = (x3 - x1) * dy1 - (y3 - y1) * dx1

    t = num_t / denom
    u = num_u / denom

    eps = 1e-9
    if -eps <= t <= 1 + eps and -eps <= u <= 1 + eps:
        ix = x1 + t * dx1
        iy = y1 + t * dy1
        return (round(ix, 2), round(iy, 2))
    return None

def dist(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def polygon_area(vertices):
    n = len(vertices)
    area2 = 0.0
    for i in range(n):
        j = (i + 1) % n
        area2 += vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]
    return abs(area2) / 2.0

def polygon_perimeter(vertices):
    n = len(vertices)
    return sum(dist(vertices[i], vertices[(i + 1) % n]) for i in range(n))

def find_cycle(adj, n):
    """
    Finds a simple cycle of length >= 3 in the intersection graph.
    Returns the ordered list of stick indices in the cycle.
    """
    visited = [False] * n
    parent = [-1] * n

    for start_node in range(n):
        if visited[start_node]:
            continue

        cycle = []
        def dfs(u, p):
            visited[u] = True
            parent[u] = p
            for v in adj[u]:
                if v == p:
                    continue
                if visited[v]:
                    curr = u
                    c = [v]
                    while curr != v and curr != -1:
                        c.append(curr)
                        curr = parent[curr]
                    if len(c) >= 3:
                        cycle.extend(c)
                        return True
                else:
                    if dfs(v, u):
                        return True
            return False

        if dfs(start_node, -1) and cycle:
            return cycle
    return None

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    sticks = []
    idx = 1
    total_stick_length = 0.0

    for _ in range(n):
        x1, y1, x2, y2 = map(float, input_data[idx:idx+4])
        idx += 4
        sticks.append(((x1, y1), (x2, y2)))
        total_stick_length += dist((x1, y1), (x2, y2))

    # Build segment intersection graph
    adj = {i: [] for i in range(n)}
    intersections = {}

    for i in range(n):
        for j in range(i + 1, n):
            pt = segment_intersection(sticks[i][0], sticks[i][1], sticks[j][0], sticks[j][1])
            if pt is not None:
                adj[i].append(j)
                adj[j].append(i)
                intersections[(i, j)] = pt
                intersections[(j, i)] = pt

    # Find closed figure cycle
    cycle = find_cycle(adj, n)
    if not cycle or len(cycle) < 3:
        print("Abandoned", end="")
        return

    k = len(cycle)
    # Collect vertices of the polygon in cyclic order
    polygon_vertices = []
    for i in range(k):
        s1 = cycle[i]
        s2 = cycle[(i + 1) % k]
        polygon_vertices.append(intersections[(s1, s2)])

    kalyan_area = polygon_area(polygon_vertices)
    if kalyan_area <= 1e-9:
        print("Abandoned", end="")
        return

    kalyan_perimeter = polygon_perimeter(polygon_vertices)
    leftover_length = max(0.0, total_stick_length - kalyan_perimeter)

    # Maximum area computer can form is a circle with circumference = leftover_length
    computer_area = (leftover_length ** 2) / (4.0 * math.pi)

    if kalyan_area > computer_area:
        print("Kalyan", end="")
    else:
        print("Computer", end="")

if __name__ == "__main__":
    solve()