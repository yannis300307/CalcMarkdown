import base64
import math
from PIL import Image

def compress(d):
  final_data=""
  last=""
  count=1
  for current_index in range(len(d)+1):
    if current_index==len(d):
      char=""
    else:
      char=d[current_index]
    if last==char and count < 4095 :
      count+=1
    else:
      co=hex(count)[2:]
      if count>5:
        final_data+="°"+(3-len(co))*"0"+co+str(last)
      else:
        final_data+=last*count
      count=1
    last=char
  return final_data

file_name = input("file ? ")
lines_count = int(input("lines count ? "), )

img = Image.open(file_name)

img = img.convert("RGB")

line_height = img.height // lines_count

print("width:" , img.width)
print("height:", line_height)

y_offset = 1

for i in range(lines_count):
    current_line = img.crop((0, i*line_height + y_offset, img.width, i*line_height+line_height+y_offset))

    current_line.show()

    data = 0
    j=0
    for x in range(current_line.width):
        for y in range(current_line.height):
            if sum(current_line.getpixel((x, y))) > 382:
                data |= (1<<j)

            j+=1

    print(f"line{i}=\""+compress(base64.b64encode(data.to_bytes(int(math.log2(data)+1), "big")).decode())+"\"")

    # data & 1 << y+x*img.height != 0

img.close()
