import json
import math
import time
import pygame

def draw_line(x1, y1, x2, y2, width, color):
    if x2 < x1:
        x1, y1, x2, y2, = x2, y2, x1, y1
    xo = x2-x1
    yo = y2-y1
    y_error = yo/xo if xo != 0 else yo
    half_width = width/2

    if xo == 0:
        if yo > 0:
            pygame.draw.rect(wd, color, (x1-int(half_width), y1-half_width, width, yo+width))
        else:
            pygame.draw.rect(wd, color, (x1-int(half_width), y2-half_width, width, -yo+width))
        return
    
    y_width = abs(math.ceil(y_error)) if abs(y_error) > width else width

    for i in range(xo+1):
        y = math.ceil(y1+i*y_error-half_width)

        ny_width = y_width
        if i == xo and y2 > y1:
            ny_width = width
        if i == 0 and y2 < y1 and y+y_width > y1:
            ny_width = width

        pygame.draw.rect(wd, color, (int(x1+i-half_width), y, width, ny_width))


LETTERS = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

inp = input("> ")
if inp:
    letters_points = json.loads(inp)
else:
    letters_points = {}

pygame.init()

wd = pygame.display.set_mode((500, 500))

running = True

point_num = 0

font = pygame.font.SysFont("Arial", 400)

current_letter_i = 0

if LETTERS[current_letter_i] not in letters_points:
    letters_points[LETTERS[current_letter_i]] = []
points = letters_points[LETTERS[current_letter_i]]

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                points.append(e.pos)
                point_num += 1
            elif e.button == 2 and point_num % 2 == 0:
                point_num -= 1
                points.pop(-1)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                if current_letter_i > 0:
                    current_letter_i -= 1
                    if LETTERS[current_letter_i] not in letters_points:
                        letters_points[LETTERS[current_letter_i]] = []
                    points = letters_points[LETTERS[current_letter_i]]
            if e.key == pygame.K_RIGHT:
                if current_letter_i < len(LETTERS)-1:
                    current_letter_i += 1
                    if LETTERS[current_letter_i] not in letters_points:
                        letters_points[LETTERS[current_letter_i]] = []
                    points = letters_points[LETTERS[current_letter_i]]
                
    if not running:
        break

    wd.fill((255, 255, 255))
    img = font.render(LETTERS[current_letter_i], False, (150, 150, 150))
    wd.blit(img, (250-img.get_width()//2, 0))

    for i in range(len(points)):
        if i % 2 == 1:
            draw_line(*points[i-1], *points[i], 50, (0, 0, 0))
        elif i == len(points)-1:
            draw_line(*points[i], *pygame.mouse.get_pos(), 50, (200, 200, 0))

    pygame.display.update()
    time.sleep(0.02)

print(json.dumps(letters_points))

for i in letters_points.keys():
    normalised = [(round(i[0]/500*255), round(i[1]/500*255)) for i in letters_points[i]]

    letters_points[i] = ".".join([str(i[0])+"."+str(i[1]) for i in normalised])

print()
print()
print()
print(letters_points)