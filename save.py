import math
import kandinsky

def draw_line(x1, y1, x2, y2, width, color):
    if x2 < x1:
        x1, y1, x2, y2, = x2, y2, x1, y1
    xo = x2-x1
    yo = y2-y1
    y_error = yo*1/xo

    print((xo/yo))

    if width == 1:
        if xo == 0:
            kandinsky.fill_rect(x1, y1, 1, y2-y1, color)
            return
        if abs(y_error) <= 1:
            for i in range(xo+1):
                kandinsky.set_pixel(x1+i, int(y1+i*y_error), color)
        else:
            for i in range(xo+1):
                kandinsky.fill_rect(int(x1+i), int(y1+i*y_error), 1, math.ceil(y_error), color)
        return

    left_offset = width//2
    right_offset = math.ceil(width/2)
    if xo == 0:
        kandinsky.fill_rect(x1-left_offset, y1, right_offset, y2-y1, color)
        return
    
    x1-=left_offset

    for j in range(left_offset, left_offset+right_offset):
        for i in range(xo+1):
            kandinsky.fill_rect(int(x1+i), int(y1+i*y_error), 1, math.ceil(y_error), color)
        x1 += 1
        y1 += -xo/yo

draw_line(200, 10, 40, 200, 30, (0, 0, 0))


# 2
import math
import kandinsky

def draw_line(x1, y1, x2, y2, width, color):
    if x2 < x1:
        x1, y1, x2, y2, = x2, y2, x1, y1
    xo = x2-x1
    yo = y2-y1
    y_error = yo*1/xo

    print((xo/yo))

    if width == 1:
        if xo == 0:
            kandinsky.fill_rect(x1, y1, 1, y2-y1, color)
            return
        if abs(y_error) <= 1:
            for i in range(xo+1):
                kandinsky.set_pixel(x1+i, round(y1+i*y_error), color)
        else:
            for i in range(xo+1):
                kandinsky.fill_rect(int(x1+i), round(y1+i*y_error), 1, math.ceil(y_error), color)
        return

    left_offset = width//2
    right_offset = math.ceil(width/2)
    if xo == 0:
        kandinsky.fill_rect(x1-left_offset, y1, right_offset, y2-y1, color)
        return
    
    for i in range(xo+1):
        for j in range(width):
            for je in range(math.ceil(y_error)):
                draw_line(int(x1+i), round(y1+i*y_error+je), int(x1+i-width*(yo/xo)), round(y1+i*y_error+width+je), 1, color)

line = (20, 20, 60, 100)
draw_line(line[0], line[1], line[2], line[3], 5, (0, 0, 0))
draw_line(line[0], line[1], line[2], line[3], 1, (255, 0, 0))
