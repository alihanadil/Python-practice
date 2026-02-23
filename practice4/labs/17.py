import math

def solve():
    # Read inputs (as floats, but they may be integers)
    R = float(input().strip())
    x1, y1 = map(float, input().split())
    x2, y2 = map(float, input().split())

    # Vector from A to B
    dx = x2 - x1
    dy = y2 - y1
    seg_len = math.hypot(dx, dy)      # length of the whole segment
    R2 = R * R

    # Squared distances of endpoints from origin
    dA2 = x1*x1 + y1*y1
    dB2 = x2*x2 + y2*y2

    # Both endpoints inside (or on) the circle → whole segment inside
    if dA2 <= R2 and dB2 <= R2:
        print(f"{seg_len:.10f}")
        return

    # Degenerate segment (A and B coincide)
    if seg_len == 0.0:
        print("0.0000000000")
        return

    # Coefficients of the quadratic: a*t^2 + b*t + c = 0
    a = dx*dx + dy*dy          # >0 because seg_len>0
    b = 2.0 * (x1*dx + y1*dy)
    c = dA2 - R2

    disc = b*b - 4.0*a*c
    if disc < 0:
        # No real intersection → both endpoints outside, no part inside
        print("0.0000000000")
        return

    # If discriminant is very small due to numerics, treat as zero (tangent)
    if disc <= 0:
        # Single touching point → length zero
        print("0.0000000000")
        return

    sqrt_disc = math.sqrt(disc)
    t1 = (-b - sqrt_disc) / (2.0*a)
    t2 = (-b + sqrt_disc) / (2.0*a)
    # Ensure t1 <= t2
    if t1 > t2:
        t1, t2 = t2, t1

    # Intersection of [t1, t2] with the segment parameter interval [0, 1]
    t_start = max(0.0, t1)
    t_end = min(1.0, t2)

    if t_start < t_end:
        inside_len = seg_len * (t_end - t_start)
    else:
        inside_len = 0.0

    print(f"{inside_len:.10f}")

solve()    