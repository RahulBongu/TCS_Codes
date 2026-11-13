import sys

def solve():
    lines = sys.stdin.read().splitlines()
    lines = [line for line in lines if line != '']

    if len(lines) < 9:
        return

    digit_rows = lines[:3]
    op_rows = lines[3:6]
    expr_rows = lines[6:9]

    def pattern(rows, index, offset, stride):
        start = offset + index * stride
        bits = []

        for row in rows:
            for j in range(3):
                pos = start + j
                ch = row[pos] if pos < len(row) else ' '
                bits.append('1' if ch != ' ' else '0')

        return ''.join(bits)

    # Find a layout that correctly recognizes every expression symbol.
    layout = None
    last = max(
        (i for row in expr_rows
         for i, ch in enumerate(row) if ch != ' '),
        default=-1
    )

    candidates = [(0, 4)]
    candidates += [
        (offset, stride)
        for stride in (4, 3, 5)
        for offset in range(stride)
        if (offset, stride) != (0, 4)
    ]

    for offset, stride in candidates:
        dm = {
            pattern(digit_rows, i, offset, stride): str(i)
            for i in range(10)
        }

        symbols = ['OR', 'AND', 'NOT', '(', ')']
        om = {
            pattern(op_rows, i, offset, stride): symbols[i]
            for i in range(5)
        }

        if len(dm) != 10 or len(om) != 5:
            continue

        if set(dm) & set(om):
            continue

        count = (last - offset) // stride + 1
        if count <= 0:
            continue

        valid = True
        for i in range(count):
            p = pattern(expr_rows, i, offset, stride)
            if p not in dm and p not in om:
                valid = False
                break

        if valid:
            layout = (offset, stride, dm, om, count)
            break

    if layout is None:
        return

    offset, stride, digit_map, op_map, count = layout

    tokens = []
    value = 0
    width = 0

    for i in range(count):
        p = pattern(expr_rows, i, offset, stride)

        if p in digit_map:
            value = (value << 9) | int(p, 2)
            width += 9
        else:
            if width:
                tokens.append(('NUM', value, width))
                value = 0
                width = 0
            tokens.append(op_map[p])

    if width:
        tokens.append(('NUM', value, width))

    # Precedence: parentheses, NOT, OR, AND.
    pos = 0

    def primary():
        nonlocal pos

        if tokens[pos] == '(':
            pos += 1
            result = parse_and()
            pos += 1
            return result

        token = tokens[pos]
        pos += 1
        return token[1], token[2]

    def unary():
        nonlocal pos

        if pos < len(tokens) and tokens[pos] == 'NOT':
            pos += 1
            value, width = unary()
            return (~value) & ((1 << width) - 1), width

        return primary()

    def parse_or():
        nonlocal pos

        value, width = unary()

        while pos < len(tokens) and tokens[pos] == 'OR':
            pos += 1
            other, other_width = unary()
            width = max(width, other_width)
            value |= other

        return value, width

    def parse_and():
        nonlocal pos

        value, width = parse_or()

        while pos < len(tokens) and tokens[pos] == 'AND':
            pos += 1
            other, other_width = parse_or()
            width = max(width, other_width)
            value &= other

        return value, width

    result, width = parse_and()
    bits = format(result, '0{}b'.format(width))

    answer = []
    for i in range(0, width, 9):
        p = bits[i:i + 9]
        answer.append(digit_map[p])

    sys.stdout.write(str(int(''.join(answer))))


if __name__ == "__main__":
    solve()