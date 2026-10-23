import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    
    horizontal_lines = []
    vertical_lines = []
    
    idx = 1
    for _ in range(n):
        x1 = int(input_data[idx])
        y1 = int(input_data[idx + 1])
        x2 = int(input_data[idx + 2])
        y2 = int(input_data[idx + 3])
        idx += 4
        
        if y1 == y2 and x1 != x2:
            horizontal_lines.append((y1, min(x1, x2), max(x1, x2)))
        elif x1 == x2 and y1 != y2:
            vertical_lines.append((x1, min(y1, y2), max(y1, y2)))
            
    def intersects(h, v):
        hy, hx1, hx2 = h
        vx, vy1, vy2 = v
        return (hx1 <= vx <= hx2) and (vy1 <= hy <= vy2)

    rectangles = set()
    num_h = len(horizontal_lines)
    num_v = len(vertical_lines)
    
    for i in range(num_h):
        for j in range(i + 1, num_h):
            h1 = horizontal_lines[i]
            h2 = horizontal_lines[j]
            if h1[0] == h2[0]:
                continue  # Must be at different y-levels
                
            for k in range(num_v):
                for l in range(k + 1, num_v):
                    v1 = vertical_lines[k]
                    v2 = vertical_lines[l]
                    if v1[0] == v2[0]:
                        continue  # Must be at different x-levels
                        
                    # Verify all four corner intersections exist
                    if (intersects(h1, v1) and 
                        intersects(h1, v2) and 
                        intersects(h2, v1) and 
                        intersects(h2, v2)):
                        
                        x_min = min(v1[0], v2[0])
                        x_max = max(v1[0], v2[0])
                        y_min = min(h1[0], h2[0])
                        y_max = max(h1[0], h2[0])
                        
                        rectangles.add((x_min, x_max, y_min, y_max))
                        
    sys.stdout.write(str(len(rectangles)))

if __name__ == '__main__':
    solve()