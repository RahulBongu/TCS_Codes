import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    pts = []
    idx = 1
    for _ in range(n):
        x = int(input_data[idx])
        y = int(input_data[idx + 1])
        pts.append((x, y))
        idx += 2
        
    # 1. Calculate original Area using Shoelace formula
    shoelace = 0
    for i in range(n):
        j = (i + 1) % n
        shoelace += pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]
    area_0 = abs(shoelace) / 2.0

    # 2. Calculate edge lengths and perimeter
    perimeter = 0.0
    min_edge = float('inf')
    for i in range(n):
        j = (i + 1) % n
        edge_len = abs(pts[j][0] - pts[i][0]) + abs(pts[j][1] - pts[i][1])
        perimeter += edge_len
        if edge_len < min_edge:
            min_edge = edge_len

    # 3. Determine maximum steps k where H = 0.1 * k
    # Condition: edge_len - 2 * (0.1 * k) >= 0.1  =>  0.2 * k <= edge_len - 0.1
    # 2 * k <= 10 * edge_len - 1
    max_k = int((10 * min_edge - 1) // 2)

    # 4. Search for maximum volume
    max_volume = 0.0
    for k in range(1, max_k + 1):
        h = round(k * 0.1, 5)
        base_area = area_0 - perimeter * h + 4.0 * (h ** 2)
        if base_area > 0:
            volume = base_area * h
            if volume > max_volume:
                max_volume = volume

    print(f"{max_volume:.2f}", end="")

if __name__ == '__main__':
    solve()