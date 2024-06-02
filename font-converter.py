import base64
import math
import zlib
from PIL import Image

def compress(d):
  fd=""
  l=""
  c=1
  for ci in range(len(d)+1):
    if ci==len(d):
      i=""
    else:
      i=d[ci]
    if l==i:
      c+=1
    else:
      co=str(c)
      if c>5:
        fd+="°"+(3-len(co))*"0"+co+str(l)
      else:
        fd+=l*c
      c=1
    l=i
  return fd

file_name = input("file ? ")
lines_count = int(input("lines count ? "), )

img = Image.open(file_name)

img = img.convert("RGB")

line_height = img.height // lines_count

print("width:" , img.width)
print("height:", line_height)

for i in range(lines_count):
    current_line = img.crop((0, i*line_height, img.width, i*line_height+line_height))

    data = 0
    j=0
    for x in range(current_line.width):
        for y in range(current_line.height):
            if sum(current_line.getpixel((x, y))) > 382:
                data |= (1<<j)

            j+=1

    current_line

    print(f"line{i}=\""+compress(base64.b64encode(data.to_bytes(int(math.log2(data)+1), "big")).decode())+"\"")

    # data & 1 << y+x*img.height != 0

img.close()
