import math

from PIL import Image, ImageDraw

from insutil import *


def rgb_to_greyscale(rgb: tuple[int, int, int]):
    return 0.3*rgb[0] + 0.59*rgb[1] + 0.11*rgb[2]

# rounds a greyscale value (single int) to a finite set of values, usually between 0-255
def round_to_band(value, bands):
    band_size = 256 / bands
    return round(value / band_size)


orig_input = Image.open("./japan-edited.jpg")

# get transparent to white
# orig_input.load()
# background = Image.new("RGB", orig_input.size, (0, 255, 0))
# background.paste(orig_input, mask=orig_input.split()[3]) # 3 is the alpha channel
# orig_input = background
# orig_input.save("./orig.jpg")



orig_w, orig_h = orig_input.width, orig_input.height
print(f"orig width:{orig_w} and orig height:{orig_h}")

x_margin = 20
y_margin = 66
page_width = 210
page_height = 297
num_shades = 32
pixels_mm = 1
pixel_samples = 7

# total possible dimensions
max_width = page_width - 2 * x_margin
max_height = page_height - 2 * y_margin

# try scale by width
aspect_scale = max_width / orig_w
if aspect_scale * orig_h > max_height:
    aspect_scale = max_height / orig_h

aspect_scale *= pixels_mm

scaled_width = int(round(orig_w * aspect_scale))
scaled_height = int(round(orig_h * aspect_scale))
scaled_image = orig_input.resize((scaled_width, scaled_height), resample=0)

for x in range(scaled_width):
    for y in range(scaled_height):
        greyscale = rgb_to_greyscale(scaled_image.getpixel((x, y)))
        greyscale = round_to_band(greyscale, num_shades)
        scaled_image.putpixel((x, y), (greyscale, greyscale, greyscale))

print(f"scaled width:{scaled_width} and scaled height:{scaled_height}")


# image manip done, now draw image


plt_x = x_margin
plt_y = y_margin
pc = PaperCanvas(plt_x, plt_y, (754 - 210) / 1.98, 192.0, 754)



for column in range(scaled_height):
    for row in range(scaled_width):
        ltr = column % 2 == 0

        darkness = (scaled_image.getpixel((row, column)) if ltr else scaled_image.getpixel((scaled_width - row - 1, column)))[0]
        shade = num_shades - darkness # num between 0 <-> num_shades
        y_mod = 0

        for s in range(pixel_samples):
            if ltr:
                plt_x += 1 / (pixels_mm * pixel_samples)
            else:
                plt_x -= 1 / (pixels_mm * pixel_samples)

            y_mod = math.sin(plt_x * math.pi * 2 * shade / 5) * (shade / num_shades * 0.9)

            pc.goto(plt_x, min(plt_y + y_mod, scaled_height + y_margin))
            pc.sample()

    plt_y += 1 / pixels_mm

    pc.goto(plt_x, max(y_margin, min(plt_y, scaled_height + y_margin)))
    pc.sample()



pc.pop_sample()
print(f"last y: {pc.current_y}")

ins = pc.gen_instructions()

with open("../sim-rs/ins.json", "w") as fp:
    fp.write(ins)




exit(1)





print(input.getpixel((0,0)))
print(rgb_to_greyscale(input.getpixel((0,0))))


output = Image.new(mode="RGB", size=(input_w, input_h))
pixels = output.load()

for x in range(input_w):
    for y in range(input_h):
        greyscale = rgb_to_greyscale(input.getpixel((x, y)))
        greyscale = int(round(greyscale))
        pixels[x, y] = (greyscale, greyscale, greyscale)

# output.show()
# now we have the image pixels as greyscale, we can manipulate it.


color_shades = 16
bands = 120
y_per_band = int(round(input_h / bands))
shrunk_image = Image.new(mode="RGB", size=(int(round(input_w / y_per_band)), int(round(input_h / y_per_band))))
shrunk_pixels = shrunk_image.load()
for y in range(0, int(round(input_h / y_per_band))):
    for x in range(0, int(round(input_w / y_per_band))):
        total_greyscale = 0


        for i in range(y_per_band):
            for j in range(y_per_band):
                total_greyscale += pixels[x * y_per_band + j, y * y_per_band + i][0]

        avg_greyscale = int(round(total_greyscale / (y_per_band ** 2)))
        avg_greyscale = round_to_band(avg_greyscale, color_shades - 1)
        
        shrunk_pixels[x,y] = (avg_greyscale, avg_greyscale, avg_greyscale)


# measurements in mm
x_margin = 20
y_margin = 20


# shrunk_image.show()
# now we have pixelated the image into 16 colour shades

