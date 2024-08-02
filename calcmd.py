import math
import kandinsky

def draw_line(x1, y1, x2, y2, width, color):
    if x2 < x1:
        x1, y1, x2, y2, = x2, y2, x1, y1
    xo = x2-x1
    yo = y2-y1
    y_error = yo/xo if xo != 0 else yo
    half_width = width/2

    if xo == 0:
        if yo > 0:
            kandinsky.fill_rect(x1-int(half_width), int(y1-half_width), width, yo+width, color)
        else:
            kandinsky.fill_rect(x1-int(half_width), int(y2-half_width), width, -yo+width, color)
        return
    
    y_width = abs(math.ceil(y_error)) if abs(y_error) > width else width

    for i in range(xo+1):
        y = math.ceil(y1+i*y_error-half_width)

        ny_width = y_width
        if i == xo and y2 > y1:
            ny_width = width
        if i == 0 and y2 < y1 and y+y_width > y1:
            ny_width = width

        kandinsky.fill_rect(int(x1+i-half_width), y, width, ny_width, color)

def draw_letter(l, x, y, size, weight, color=(0, 0, 0)):
    if l in letters:
        points = letters[l].split(".")
        
        for i in range(3, len(points), 4):
            draw_line(round(x+int(points[i-3], 16)/255*size), 
                      round(y+int(points[i-2], 16)/255*size), 
                      round(x+int(points[i-1], 16)/255*size), 
                      round(y+int(points[i], 16)/255*size), 
                      weight, color)

def render_md_line(text, x, y, size, weight, spacing, allow_bold=False):
    active_bold = False
    active_strike = False
    render_cursor = 0
    reading_cursor = 0
    while reading_cursor < len(text):
        skip = False
        if allow_bold and text[reading_cursor] == "*" and text[reading_cursor+1] == "*":
            if active_bold:
                active_bold = False
                render_cursor -= 1
                reading_cursor += 1
            else:
                active_bold = True
                render_cursor -= 1
                reading_cursor += 1
            skip = True
        if text[reading_cursor] == "~" and text[reading_cursor+1] == "~":
            if active_strike:
                active_strike = False
                render_cursor -= 1
                reading_cursor += 1
            else:
                active_strike = True
                render_cursor -= 1
                reading_cursor += 1
            skip = True
        if not skip:
            draw_letter(text[reading_cursor], x+render_cursor*spacing, y, size, weight+1 if active_bold else weight)
            if active_strike:
                draw_line(x+render_cursor*spacing, y+size/2, x+render_cursor*spacing+spacing, y+size/2, 1, (0, 0, 0))
        render_cursor += 1
        reading_cursor += 1
            
    return x+reading_cursor*spacing

def parse_md_line(text, y, x_offset=0, color=(0, 0, 0)):
    words = text.split()
    if words[0] == "#":
        render_md_line(text[2:], x_offset+0, y, 50, 5, 18)
        draw_line(x_offset + 10, y+45, 310 - x_offset, y+45, 1, (200, 200, 200))
        return 50
    elif words[0] == "##":
        render_md_line(text[3:], x_offset+5, y, 35, 4, 16)
        draw_line(x_offset + 10, y+35, 310 - x_offset, y+35, 1, (200, 200, 200))
        return 40
    elif words[0] == "###":
        render_md_line(text[4:], x_offset+10, y, 25, 3, 15)
        return 30
    elif words[0] == ">":
        height = parse_md_line(text[2:], y, x_offset+20)
        kandinsky.fill_rect(x_offset+15, y, 4, height, (200, 200, 200))
        return height
    else:
        render_md_line(text, x_offset+5, y, 18, 2, 10, True)
        return 15

letters = {' ': '', '!': '80.28.81.8b.80.a7.80.b1', '"': '6e.27.6d.50.8f.25.8d.52', '#': 'a5.25.89.af.54.b5.74.2c.4a.55.b2.57.47.88.ae.8a', '$': '9e.46.98.32.98.32.87.2b.86.2b.72.2d.72.2d.60.3a.60.3a.59.4f.59.53.5f.63.5f.63.9b.7a.9b.7a.a5.94.a5.94.9c.a9.9c.a9.88.b4.88.b4.74.b4.74.b4.5f.ab.5f.ab.58.9b.7c.1a.7d.c9', '%': '38.3a.38.5b.38.5b.3e.6b.3e.6b.5a.6b.5a.6b.68.56.68.56.68.39.68.39.5d.28.5c.28.4a.28.4a.28.37.33.98.87.98.a9.98.a9.a6.b7.a6.b8.b7.b8.b7.b8.c5.a4.c5.a4.c4.87.c4.87.bd.7c.bd.7c.b0.79.b0.79.97.86.a5.25.5b.b8', '&': 'b7.b5.61.4c.61.4b.61.36.61.36.77.28.77.28.8c.2e.8c.2e.96.43.96.43.91.54.91.54.55.82.55.82.4e.97.4e.97.58.af.59.af.72.b8.73.b8.93.ac.93.ac.a9.82', "'": '7f.29.7f.50', '(': '92.26.7f.49.7e.4a.76.73.76.73.76.a3.76.a3.81.d1.81.d1.90.de', ')': '72.25.8c.55.8c.55.94.84.94.84.8c.bb.8c.bc.75.dd', '*': '5a.37.a3.5a.97.25.70.6f.76.22.8e.6e.a7.3a.5c.59', '+': '7e.41.7e.96.52.70.a8.6f', ',': '84.a6.7c.b9.7c.b9.71.c6', '-': '65.84.94.84', '.': '7e.ab.7f.ad', '/': '95.24.65.b6', '0': '56.55.57.96.57.96.6e.b2.6e.b2.8b.b5.8b.b5.a4.9f.a4.9f.a4.54.a4.54.9d.36.9d.36.86.2c.86.2c.6d.35.6d.35.57.54', '1': '5c.53.88.31.88.31.8d.b1', '2': '5b.50.6c.32.6c.32.80.2b.80.2b.a2.38.a2.38.a7.5b.a7.5b.5a.b2.5a.b2.a4.b0', '3': '5b.4d.70.2f.70.2f.95.2e.95.2e.a7.4c.a7.4c.93.63.93.63.7f.6c.7f.6c.9c.75.9c.75.ad.8c.ad.8c.9f.ac.9f.ac.88.b8.88.b8.6a.b2.6a.b2.5b.9c', '4': '90.b7.91.32.91.32.4f.8f.4f.8f.a3.8e', '5': 'a6.30.68.30.68.30.5a.6d.5a.6d.7d.60.7d.60.92.61.93.61.a3.75.a3.75.aa.97.aa.97.96.b0.96.b0.7c.b6.7c.b6.64.a9.64.a9.59.9b', '6': 'a5.4a.95.30.94.2f.76.2e.76.2e.5c.47.5c.47.53.78.54.77.5f.a8.5f.a8.78.b8.78.b8.a1.ae.a1.ae.a7.8e.a7.8e.a7.76.a7.76.94.68.94.68.79.68.79.68.5e.7c', '7': '52.2e.ac.2e.ab.2e.6e.b4.68.6d.bb.6b', '8': '6c.69.95.69.95.69.a2.4f.a2.4f.99.35.99.35.88.2b.88.2b.6d.31.6d.31.5b.44.5b.44.68.69.67.6f.58.85.58.85.5b.a8.5b.a8.73.b7.74.b7.8d.b7.8e.b7.a7.a4.a7.a4.a7.8a.a7.8a.8f.69', '9': '5a.98.73.b7.73.b7.8f.b6.8f.b6.a0.9a.a0.9a.a7.63.a7.63.9a.3a.9a.3a.80.2f.80.2f.60.38.60.38.57.59.57.59.60.76.60.76.7e.7c.7e.7c.a2.65', ':': '80.56.80.5b.81.ac.81.ae', ';': '7e.58.7e.5c.80.a6.7e.b7.7e.b7.74.c6', '<': 'ae.48.57.72.57.72.a7.99', '=': '50.5a.a5.5a.4e.85.a7.85', '>': '4e.47.a6.6f.a6.6f.50.99', '?': '5a.4f.6c.31.6c.31.85.29.85.29.a2.36.a2.36.a4.50.a4.50.97.68.95.69.82.78.82.78.82.90.7e.ad.7e.ae', '@': 'a7.53.98.ac.98.ac.af.af.af.af.cc.9b.cc.9b.d7.77.d7.77.d2.54.d2.54.c6.39.c6.39.9f.2b.9f.2b.7d.2a.7a.2a.4f.37.4f.38.2f.5c.2f.5c.29.88.29.88.2e.af.2f.b0.48.d1.48.d1.6c.dd.6f.de.91.dd.91.dd.b6.d2.b6.d2.da.c0.98.68.8c.56.8c.56.72.58.72.58.5e.6d.5e.6d.51.8d.51.8d.5c.aa.5d.ab.74.b3.75.b3.9d.9c', 'A': '46.b8.7c.32.7c.32.ba.b9.64.87.98.87', 'B': '52.2e.52.af.52.af.91.af.91.af.ab.a4.ab.a4.b0.8b.b0.8b.a5.77.a5.77.8f.6f.8f.6f.5e.6f.8d.6d.a5.61.a5.61.aa.46.aa.46.a0.35.a0.35.8a.2d.8a.2d.5a.2e', 'C': 'b4.51.a9.38.a9.38.91.2b.91.2b.7b.2a.7b.2a.67.34.67.34.53.49.53.49.4b.66.4b.66.4c.91.4c.91.64.b0.64.b0.86.b6.86.b6.a7.aa.a7.aa.b6.8d', 'D': '4e.27.4e.b5.4e.b5.8c.b4.8c.b4.a6.a6.a6.a6.b8.83.b8.83.b7.59.b7.59.af.43.af.43.9b.30.9b.30.80.29.80.29.51.2a', 'E': 'b2.2f.57.2f.57.2f.57.af.57.af.ac.af.58.6c.ac.6c', 'F': '5c.b2.5c.2f.5c.2f.aa.2f.59.6f.a8.6f', 'G': '86.76.ba.76.ba.76.ba.9a.ba.9a.b4.a7.b4.a7.9f.b1.9f.b1.89.b5.89.b5.73.b5.73.b5.62.aa.62.aa.4c.98.4c.98.46.7b.46.7b.46.59.46.59.52.43.52.43.6e.2e.6e.2e.97.2e.97.2e.ac.3b.ac.3b.b5.4a', 'H': '4f.2d.4f.b0.af.2d.af.b1.50.6b.ab.6b', 'I': '80.27.80.af', 'J': '98.29.98.9f.98.9f.8e.ae.8e.ae.82.b5.82.b5.70.b5.70.b5.63.a9.63.a9.5d.99', 'K': '53.27.53.b1.5a.7c.b7.29.7d.68.ad.b0', 'L': '5e.27.5e.ae.5e.ae.a9.ae', 'M': '43.af.43.32.53.2e.7d.b0.7d.b0.b4.34.bd.2b.be.af', 'N': '4d.b0.4d.32.53.2c.aa.b0.af.b0.af.31', 'O': '44.59.44.8d.44.8d.53.a9.53.a9.72.b8.72.b8.93.ba.93.ba.b4.a5.b4.a5.be.85.be.85.bf.59.bf.59.b0.44.47.51.57.3d.57.3d.6f.30.6f.30.8f.30.8f.30.b1.44', 'P': '54.2f.54.af.54.74.9d.75.9d.75.b0.60.b0.60.b0.44.b0.44.9d.31.9d.31.88.2d.87.2e.58.2f', 'Q': '4b.4a.43.63.43.63.43.8b.43.8b.53.a7.53.a7.6f.b7.6f.b7.8c.b7.8c.b7.ab.a2.ab.a2.ba.7d.ba.7d.ba.58.ba.58.a7.37.a7.37.8c.2e.8c.2e.6a.2d.6a.2d.4b.4a.83.94.bc.ba', 'R': '4f.b1.4f.31.4e.2d.9b.2d.9b.2d.af.44.af.44.af.61.af.61.9c.6f.9a.71.5e.73.91.79.bc.b7', 'S': 'ac.4e.a2.37.9f.32.81.2c.7e.2c.5d.34.5d.34.50.50.50.50.5f.69.5f.69.a5.7e.a5.7e.b3.94.b3.95.a8.ab.a8.ab.93.b4.93.b4.77.b4.77.b4.5c.a6.5c.a6.51.93', 'T': '45.2e.b0.2e.7d.31.7d.ae', 'U': '4f.28.4f.9b.4f.9b.64.b5.64.b5.8c.b5.8c.b5.a6.ae.a6.ae.b4.88.b4.88.b2.2b', 'V': '46.28.80.b0.80.b0.bb.26', 'W': '2b.27.52.b2.52.b2.7b.32.7f.2c.ad.b0.ad.b0.d1.30', 'X': 'b1.27.46.b4.4d.27.ba.b2', 'Y': '48.27.7f.78.7f.78.b8.2a.7d.77.7d.b5', 'Z': '4f.2e.b0.2f.b0.2f.52.b1.52.b1.af.b1', '[': '9b.2d.7b.2d.7b.2d.7b.d7.7b.d7.95.d7', '\\': '68.26.90.b2', ']': '68.2c.89.2c.89.2c.89.d6.89.d6.69.d6', '^': '5b.75.7e.2d.7e.2d.a4.74', '_': '43.d9.b2.d9', '`': '74.27.86.3e', 'a': '5a.6e.67.5a.67.5a.80.50.80.50.9f.57.9f.57.a6.b0.9b.78.63.8c.63.8c.57.9d.57.9d.66.b9.66.b9.85.b4.85.b4.a4.90', 'b': '5c.29.5c.b3.68.61.89.58.89.58.a2.64.a2.64.a9.8f.a9.8f.9d.ae.9c.ae.83.b4.83.b4.5d.a0', 'c': 'a4.6d.9c.57.9c.57.82.52.82.52.68.62.68.62.5e.7d.5e.7d.62.9e.62.9e.70.b0.70.b0.86.b8.86.b8.a4.ab.a4.ab.a6.9b', 'd': 'a1.28.a1.b1.98.62.81.53.81.53.63.5f.63.5f.56.7c.56.7c.5a.9e.5a.9e.6d.b4.6d.b4.8d.b5.8d.b5.9d.a3', 'e': '55.81.a5.81.a5.81.a5.66.a4.66.98.5a.98.5a.83.55.83.55.71.59.6b.5a.5c.6a.5c.6a.5a.9b.59.9e.6b.ae.6b.ae.8a.b4.8a.b4.a6.a5', 'f': '9b.2c.85.2b.85.2b.79.39.79.39.7b.ae.62.53.91.53', 'g': 'a3.51.a3.ce.a3.ce.8d.e1.8d.e1.72.e2.72.e2.61.dc.61.dc.5c.ce.97.62.89.56.89.56.74.56.73.56.56.62.56.62.5a.a2.5a.a2.7a.b5.7a.b4.a3.a3', 'h': '5b.27.5b.b1.61.64.81.57.81.57.9a.57.9a.57.9f.69.9f.69.9f.af', 'i': '82.26.82.2f.7e.4f.7e.b1', 'j': '83.2d.83.34.84.50.84.d1.84.d1.78.dc.78.dc.65.dd', 'k': '62.27.62.b4.65.85.a4.4f.7e.7b.a2.af', 'l': '80.27.80.b0', 'm': '40.50.40.af.3e.68.62.56.62.56.7b.55.7b.55.80.6b.80.6b.80.af.86.64.a4.55.a4.55.bb.56.bb.56.c2.6a.c2.6a.c2.b1', 'n': '5a.50.5a.af.5e.69.81.53.81.53.91.53.91.53.a2.5f.a2.5f.a2.ae', 'o': '57.6e.57.9d.57.9d.6e.b0.6e.b0.8f.b2.8f.b2.aa.9c.aa.9c.aa.75.aa.75.9e.5f.9e.5f.88.56.88.56.6f.56.6f.56.57.6d', 'p': '5b.52.5b.d8.5e.68.7e.54.7e.54.96.53.96.53.a6.6d.a6.6d.a6.91.a6.91.9a.ab.98.ad.7c.b4.7c.b4.5a.9a', 'q': 'a1.50.a1.d5.a1.68.87.52.87.52.72.52.72.52.58.67.58.67.58.a4.58.a4.72.b0.72.b0.9e.a9', 'r': 'a0.5a.90.55.90.55.77.6d.6e.48.6e.af', 's': '9f.6b.96.58.96.58.82.51.82.51.69.55.69.55.5d.6f.5d.6f.63.7a.63.7a.9c.8f.9c.8f.a9.9f.a9.9f.9f.b5.9f.b5.85.ba.85.ba.6a.b3.6a.b3.5b.a2', 't': '7c.2f.7c.af.7c.af.89.b4.89.b4.9b.b4.65.53.93.53', 'u': 'a1.50.a1.af.9a.a3.7e.b5.7e.b5.69.b1.69.b1.5c.8f.5c.8f.5c.4e', 'v': '57.4f.81.ae.81.ae.a6.4d', 'w': '41.53.61.b1.61.b1.80.58.80.58.9e.b0.a0.b1.be.59', 'x': 'a1.4f.5b.b2.59.50.a7.b6', 'y': 'a8.4f.76.da.76.da.65.df.58.49.82.a7', 'z': 'aa.b2.5b.b2.5b.b2.a4.59.a4.59.56.59', '{': '9d.29.8a.2e.8a.2e.82.40.82.41.81.6e.81.6e.79.7e.79.7e.68.84.68.84.7a.8d.7a.8d.85.a2.85.a2.85.d0.85.d0.91.db.91.dc.99.db', '|': '7f.26.7f.d7', '}': '63.2b.75.30.75.30.84.41.84.41.84.70.84.70.8a.7a.8a.7a.98.7e.98.7e.8f.84.8f.84.85.95.85.95.80.b0.80.b0.7e.cf.7e.d0.76.dd.76.de.6a.de', '~': '4c.78.65.67.66.67.95.79.95.79.b5.65'}

text = ""

y_level = 10
y_level += parse_md_line("# Title 1", y_level)
y_level += parse_md_line("## Title 2", y_level)
y_level += parse_md_line("### Title 3", y_level)
y_level += parse_md_line("> # Citation", y_level)
#y_level += parse_md_line("normal text **bold** oui ~~non~~", y_level)
