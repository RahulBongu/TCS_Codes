import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    M = int(input_data[0])
    N = int(input_data[1])
    
    # Read the M x N grid
    idx = 2
    grid = []
    for _ in range(M):
        grid.append(input_data[idx : idx + N])
        idx += N
        
    K = int(input_data[idx])
    idx += 1
    instructions = input_data[idx : idx + K]
    
    def apply_gravity(g, rows, cols):
        new_g = [['.' for _ in range(cols)] for _ in range(rows)]
        for c in range(cols):
            stones = sum(1 for r in range(rows) if g[r][c] == '*')
            for r in range(rows - stones, rows):
                new_g[r][c] = '*'
        return new_g

    # Step 1: Apply gravity to the initial position
    grid = apply_gravity(grid, M, N)
    
    # Step 2: Process each rotation + gravity
    for inst in instructions:
        # Count stones in each row of the current M x N grid
        row_Counts = [row.count('*') for row in grid]
        
        # After 90-degree rotation, dimensions become N x M
        new_rows, new_cols = N, M
        
        if inst.lower() == 'right':
            # Clockwise: bottom row (M-1) becomes first column (0)
            col_counts = row_Counts[::-1]
        else:
            # Counter-clockwise: top row (0) becomes first column (0)
            col_counts = row_Counts
            
        # Build the rotated grid with gravity already applied
        new_grid = [['.' for _ in range(new_cols)] for _ in range(new_rows)]
        for c in range(new_cols):
            stones = col_counts[c]
            for r in range(new_rows - stones, new_rows):
                new_grid[r][c] = '*'
                
        grid = new_grid
        M, N = new_rows, new_cols

    # Print final box configuration
    out = [ " ".join(row) for row in grid ]
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    solve()