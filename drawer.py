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

    letters_points[i] = ".".join([hex(i[0])[2:]+"."+hex(i[1])[2:] for i in normalised])

print()
print()
print()
print(letters_points)

# current font : {" ": [], "!": [[250, 78], [252, 272], [250, 327], [250, 347]], "\"": [[216, 76], [213, 157], [281, 72], [277, 161]], "#": [[323, 73], [269, 344], [165, 355], [227, 87], [145, 167], [350, 171], [139, 266], [342, 271]], "$": [[310, 138], [299, 99], [299, 99], [264, 84], [263, 84], [223, 88], [223, 88], [188, 114], [188, 114], [175, 154], [175, 163], [187, 195], [187, 195], [303, 240], [303, 240], [324, 290], [324, 290], [306, 331], [306, 331], [266, 352], [266, 352], [228, 353], [228, 353], [187, 336], [187, 336], [173, 303], [244, 50], [245, 394]], "%": [], "&": [], "'": [], "(": [], ")": [], "*": [], "+": [], ",": [], "-": [], ".": [], "/": [], "0": [], "1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": [], "9": [], ":": [], ";": [], "<": [], "=": [], ">": [], "?": [], "@": [], "A": [[137, 361], [244, 98], [244, 98], [364, 363], [197, 265], [299, 265]], "B": [[161, 90], [161, 344], [161, 344], [285, 344], [285, 344], [336, 322], [336, 322], [346, 272], [346, 272], [323, 234], [323, 234], [281, 217], [281, 217], [185, 218], [277, 213], [324, 191], [324, 190], [334, 138], [334, 138], [314, 104], [314, 104], [271, 89], [271, 89], [177, 90]], "C": [[353, 158], [332, 110], [332, 110], [284, 84], [284, 84], [241, 82], [241, 82], [201, 101], [201, 101], [163, 144], [163, 144], [148, 200], [148, 200], [150, 285], [150, 285], [197, 346], [197, 346], [263, 356], [263, 356], [327, 334], [327, 334], [357, 277]], "D": [[153, 77], [153, 354], [153, 354], [274, 353], [274, 353], [326, 325], [326, 325], [360, 257], [360, 257], [359, 175], [359, 175], [343, 132], [343, 132], [304, 94], [304, 94], [251, 81], [251, 81], [158, 82]], "E": [[349, 93], [170, 93], [170, 93], [170, 343], [170, 343], [338, 343], [173, 211], [338, 211]], "F": [[180, 349], [180, 93], [180, 93], [333, 93], [175, 217], [329, 217]], "G": [[262, 231], [364, 231], [364, 231], [364, 302], [364, 302], [352, 328], [352, 328], [312, 347], [312, 347], [269, 354], [269, 354], [225, 354], [225, 354], [193, 334], [193, 334], [149, 299], [149, 299], [138, 242], [138, 242], [138, 175], [138, 175], [160, 131], [160, 131], [216, 91], [216, 91], [297, 91], [297, 91], [337, 115], [337, 115], [355, 145]], "H": [[155, 88], [155, 345], [344, 88], [344, 348], [156, 209], [335, 209]], "I": [[250, 77], [250, 343]], "J": [[299, 80], [299, 312], [299, 312], [278, 341], [278, 341], [254, 354], [254, 354], [220, 355], [220, 355], [195, 331], [195, 331], [183, 300]], "K": [[162, 76], [162, 348], [176, 244], [358, 81], [246, 203], [340, 345]], "L": [[185, 76], [185, 342], [185, 342], [331, 342]], "M": [[131, 343], [131, 99], [162, 91], [246, 346], [246, 346], [352, 102], [370, 84], [372, 344]], "N": [[151, 345], [151, 98], [162, 87], [333, 346], [344, 345], [344, 97]]}
