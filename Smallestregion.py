import sys

def get_min_dim(P1, P2, intervals):
    if P2 - P1 <= 1:
        return P2 - P1

    forbidden = []
    for r1, r2 in intervals:
        L = max(r1 + 1, P1 + 1)
        R = min(r2 - 1, P2 - 1)
        if L <= R:
            forbidden.append([L, R])

    if not forbidden:
        return 1

    forbidden.sort()
    merged = []
    for L, R in forbidden:
        if not merged:
            merged.append([L, R])
        else:
            if L <= merged[-1][1] + 1:
                merged[-1][1] = max(merged[-1][1], R)
            else:
                merged.append([L, R])

    if merged[0][0] > P1 + 1:
        return 1

    if merged[-1][1] < P2 - 1:
        return 1

    for i in range(len(merged) - 1):
        if merged[i + 1][0] - merged[i][1] - 1 >= 2:
            return 1

    folds = [P1]
    for i in range(len(merged) - 1):
        folds.append(merged[i][1] + 1)
    folds.append(P2)

    min_gap = P2 - P1
    for i in range(len(folds) - 1):
        gap = folds[i + 1] - folds[i]
        if gap < min_gap:
            min_gap = gap

    return min_gap

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    idx = 1

    x_intervals = []
    y_intervals = []

    for _ in range(N):
        x1 = int(input_data[idx])
        y1 = int(input_data[idx + 1])
        x2 = int(input_data[idx + 2])
        y2 = int(input_data[idx + 3])
        idx += 4

        x_intervals.append((min(x1, x2), max(x1, x2)))
        y_intervals.append((min(y1, y2), max(y1, y2)))

    px1 = int(input_data[idx])
    py1 = int(input_data[idx + 1])
    px2 = int(input_data[idx + 2])
    py2 = int(input_data[idx + 3])

    paper_x1, paper_x2 = min(px1, px2), max(px1, px2)
    paper_y1, paper_y2 = min(py1, py2), max(py1, py2)

    min_w = get_min_dim(paper_x1, paper_x2, x_intervals)
    min_h = get_min_dim(paper_y1, paper_y2, y_intervals)

    # Note the end="" to prevent trailing newline
    print(min_w * min_h, end="")

if __name__ == '__main__':
    solve()