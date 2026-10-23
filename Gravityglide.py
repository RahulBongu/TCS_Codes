import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    idx = 1

    slides_at = {}
    slides = []

    for i in range(N):
        x1 = int(input_data[idx])
        y1 = int(input_data[idx + 1])
        x2 = int(input_data[idx + 2])
        y2 = int(input_data[idx + 3])
        idx += 4

        dx = 1 if x2 > x1 else -1
        dy = 1 if y2 > y1 else -1
        length = abs(x2 - x1)

        points = set()
        for step in range(length + 1):
            px = x1 + step * dx
            py = y1 + step * dy
            points.add((px, py))
            if (px, py) not in slides_at:
                slides_at[(px, py)] = []
            slides_at[(px, py)].append(i)

        slides.append(points)

    start_x = int(input_data[idx])
    start_y = int(input_data[idx + 1])
    energy = int(input_data[idx + 2])

    def get_downward_direction(x, y):
        if (x, y) not in slides_at:
            return None
        for s_idx in slides_at[(x, y)]:
            pts = slides[s_idx]
            if (x - 1, y - 1) in pts:
                return (-1, -1)
            if (x + 1, y - 1) in pts:
                return (1, -1)
        return None

    def catches_falling_ball(x, y):
        if (x, y) not in slides_at:
            return False
        count = len(slides_at[(x, y)])
        if count >= 2:
            return True
        return get_downward_direction(x, y) is not None

    x, y = start_x, start_y

    if not catches_falling_ball(x, y):
        caught = False
        for cy in range(y - 1, 0, -1):
            if catches_falling_ball(x, cy):
                y = cy
                caught = True
                break
        if not caught:
            y = 0
            print(f"{x} {y}", end="")
            return

    while True:
        if y == 0:
            break

        count = len(slides_at.get((x, y), []))
        if count >= 2:
            cost = x * y
            if energy < cost:
                break
            energy -= cost

        down_dir = get_downward_direction(x, y)
        if down_dir is None:
            if count >= 2:
                break

            caught = False
            for cy in range(y - 1, 0, -1):
                if catches_falling_ball(x, cy):
                    y = cy
                    caught = True
                    break
            if not caught:
                y = 0
                break
            continue

        if energy < 1:
            break

        dx, dy = down_dir
        x += dx
        y += dy
        energy -= 1

    print(f"{x} {y}", end="")

if __name__ == '__main__':
    solve()