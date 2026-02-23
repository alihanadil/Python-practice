import math

def solve() -> None:
    R = float(input().strip())
    x1, y1 = map(float, input().split())
    x2, y2 = map(float, input().split())

    dx = x2 - x1
    dy = y2 - y1
    seg_len_sq = dx * dx + dy * dy

    # Degenerate case: A and B coincide
    if seg_len_sq == 0.0:
        print("0.0000000000")
        return

    # Check if the straight segment enters the circle interior
    # Find the closest point on the segment to the origin
    t0 = -(x1 * dx + y1 * dy) / seg_len_sq
    t = max(0.0, min(1.0, t0))
    cx = x1 + t * dx
    cy = y1 + t * dy
    dist_sq = cx * cx + cy * cy

    if dist_sq >= R * R:
        # Segment stays outside (or touches) – straight line is valid
        direct_len = math.sqrt(seg_len_sq)
        print(f"{direct_len:.10f}")
        return

    # Otherwise we must go around the circle
    dA = math.hypot(x1, y1)
    dB = math.hypot(x2, y2)

    # Safety clamp (points are guaranteed to be on or outside)
    dA = max(dA, R)
    dB = max(dB, R)

    alpha = math.acos(R / dA)
    beta  = math.acos(R / dB)

    thetaA = math.atan2(y1, x1)
    thetaB = math.atan2(y2, x2)

    # Four possible tangent points
    tA1 = thetaA + alpha
    tA2 = thetaA - alpha
    tB1 = thetaB + beta
    tB2 = thetaB - beta

    lenA = math.sqrt(dA * dA - R * R)
    lenB = math.sqrt(dB * dB - R * R)

    def angular_dist(a: float, b: float) -> float:
        """shortest arc length between two angles (in radians)"""
        diff = abs(a - b) % (2 * math.pi)
        if diff > math.pi:
            diff = 2 * math.pi - diff
        return diff

    best = float('inf')
    for tA in (tA1, tA2):
        for tB in (tB1, tB2):
            arc = angular_dist(tA, tB)
            total = lenA + lenB + R * arc
            if total < best:
                best = total

    print(f"{best:.10f}")

if __name__ == "__main__":
    solve()