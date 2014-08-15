import math

# Code adapted from: http://stackoverflow.com/a/23017208
def line_circle_intersect(cx, cy, radius, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    A = dx * dx + dy * dy
    B = 2 * (dx * (x1 - cx) + dy * (x1 - cy))
    C = (x1 - cx) * (x1 - cx) + (y1 - cy) * (y1 - cy) - radius * radius
    
    det = B * B - 4 * A * C
    if A <= 0.0000001 or det < 0:
        return []
    elif det == 0:
    {
        # One solution.
        t = -B / (2 * A)
        return [(y1 + t * dx, y1 + t * dy)]
    else:
        # Two solutions.
        t1 = (-B + math.sqrt(det)) / (2 * A)
        t2 = (-B - math.sqrt(det)) / (2 * A)
        return [(x1 + t1 * dx, y1 + t1 * dy), (x1 + t2 * dx, y1 + t2 * dy)]