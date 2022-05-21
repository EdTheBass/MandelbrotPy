import functools
import numpy as np
from random import randint as r
import sys


def createInterpolant(xs, ys):
    length = len(xs)

    if (length != len(ys)):
        raise ValueError("Need an equal count of xs and ys.")
    if (length == 0):
        def f(x):
            return 0
        return f
    if (length == 1):
        result = ys[0]
        def f(x):
            return result
        return f
    
    indexes = []
    for i in range(length):
        indexes.append(i)

    def g(a,b): 
        return -1 if xs[a] < xs[b] else 1
    indexes.sort(key=functools.cmp_to_key(g))

    oldXs = xs
    oldYs = ys
    xs = []
    ys = []
    for i in range(length):
        xs.append(oldXs[indexes[i]])
        ys.append(oldYs[indexes[i]])
    
    dys = []
    dxs = []
    ms = []

    for i in range(length-1):
        dx = xs[i + 1] - xs[i]
        dy = ys[i + 1] - ys[i]
        dxs.append(dx)
        dys.append(dy)
        ms.append(dy/dx)

    c1s = [ms[0]]
    for i in range(len(dxs)-1):
        m = ms[i]
        mNext = ms[i + 1]
        if m*mNext <= 0:
            c1s.append(0)
        else:
            dx_ = dxs[i]
            dxNext = dxs[i + 1]
            common = dx_ + dxNext
            c1s.append(3*common/((common + dxNext)/m + (common + dx_)/mNext))
    
    c1s.append(ms[len(ms) - 1])

    c2s = []
    c3s = []
    for i in range(len(c1s)-1):
        c1 = c1s[i]
        m_ = ms[i]
        invDx = 1/dxs[i]
        common_ = c1 + c1s[i + 1] - m_ - m_
        c2s.append((m_ - c1 - common_)*invDx)
        c3s.append(common_*invDx*invDx)

    def f(x):
        i = len(xs) - 1
        if x == xs[i]:
            return ys[i]

        low = 0
        high = len(c3s)-1
        while low <= high:
            mid = int(np.floor(0.5*(low + high)))
            xHere = xs[mid]
            if xHere < x:
                low = mid + 1
            elif xHere > x:
                high = mid - 1
            else:
                return ys[mid]
            
        i = max(0, high)

        diff = x - xs[i]
        diffSq = diff * diff
        return ys[i] + c1s[i]*diff + c2s[i]*diffSq + c3s[i]*diff*diffSq
    return f

def colours(xr, yr, xg, yg, xb, yb, x_num):
    r = createInterpolant(xr, yr)
    g = createInterpolant(xg, yg)
    b = createInterpolant(xb, yb)

    f = open("interpolated_colours.py", "w")
    red_string = "red = ["
    green_string = "green = ["
    blue_string = "blue = ["

    x = 0
    while x <= 1:
        r_val = abs(r(x))
        g_val = abs(g(x))
        b_val = abs(b(x))
        
        red_string += str(r_val if r_val <= 255 else 255) + ",\n"
        green_string += str(g_val if g_val <= 255 else 255) + ",\n"
        blue_string += str(b_val if b_val <= 255 else 255) + ",\n"

        x += 1/x_num

    red_string += "]\n\n\n"
    green_string += "]\n\n\n"
    blue_string += "]"
    
    f.write(red_string+green_string+blue_string)

# colours([0, 0.16, 0.42, 0.6425, 0.8575], [0, 32, 237, 255, 0], 
        # [0, 0.16, 0.42, 0.6425, 0.8575], [7, 107, 255, 170, 2],
        # [0, 0.16, 0.42, 0.6425, 0.8575], [100, 203, 255, 0, 0], 1000)

depth = 1000 if len(sys.argv) < 3 else int(sys.argv[2])

# ordinary colour
# colours([0, 0.16, 0.42, 0.6425, 0.8575], [0, 32, 237, 255, 0], 
        # [0, 0.16, 0.42, 0.6425, 0.8575], [7, 107, 255, 170, 2],
        # [0, 0.16, 0.42, 0.6425, 0.8575], [100, 203, 255, 0, 0], depth)

# opposite colour
# colours([0, 0.16, 0.42, 0.6425, 0.8575], [0, 255, 237, 32, 0], 
        # [0, 0.16, 0.42, 0.6425, 0.8575], [2, 170, 255, 107, 7],
        # [0, 0.16, 0.42, 0.6425, 0.8575], [0, 0, 255, 203, 100], depth)

# random
colours([0, 0.16, 0.42, 0.6425, 0.8575], [r(0, 255), r(0, 255), r(0, 255), r(0, 255), r(0, 255)], 
        [0, 0.16, 0.42, 0.6425, 0.8575], [r(0, 255), r(0, 255), r(0, 255), r(0, 255), r(0, 255)],
        [0, 0.16, 0.42, 0.6425, 0.8575], [r(0, 255), r(0, 255), r(0, 255), r(0, 255), r(0, 255)], depth)
