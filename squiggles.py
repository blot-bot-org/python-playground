import math

from PIL import Image, ImageDraw

import insutil


def rgb_to_greyscale(rgb: tuple[int, int, int]):
    return 0.3*rgb[0] + 0.59*rgb[1] + 0.11*rgb[2]

# rounds a greyscale value (single int) to a finite set of values, usually between 0-255
def round_to_band(value, bands):
    band_size = 256 / bands
    return round(value / band_size) * int(round(band_size))



input = Image.open("./bird.webp")
input_w, input_h = input.width, input.height

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
bands = 100
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
        """
        for large image: 
        for i in range(y_per_band):
            for j in range(y_per_band):
                pixels[x * y_per_band + j, y * y_per_band + i] = (avg_greyscale, avg_greyscale, avg_greyscale)
        """



# shrunk_image.show()
# now we have pixelated the image into 16 colour shades

# coeffcient between 0-1
def lerp_wave(intensity, x, y, width, coefficient):
    delta_x = (width) * coefficient + x
    delta_y = y + math.sin(intensity * 4 * delta_x) * intensity / 1.4

    return (delta_x, delta_y)


def lerp(x1, y1, x2, y2, coefficient):
    return (x1 + coefficient * (x2 - x1), y1 + coefficient * (y2 - y1))


ins = []
m_dist = 754
page_left = (m_dist - 210) / 1.98
page_top = 192
last_x, last_y = page_left, page_top
current_lbelt, current_rbelt = insutil.cartesian_to_belt(last_x, last_y, m_dist)

"""
1. Get position (disregarding previous)
2. Add page offset
3. Find belt lengths of position
4. Find delta belt lengths, using last belt lengths
5. Push delta lengths to ins
"""

# for y in range(0, bands):
width_per_wave = 190 / bands
end_at_right = True
for y in range(bands):
    end_at_right = not end_at_right
    for x in range(bands):
        val_band = int(round(shrunk_pixels[(bands - x - 1) if end_at_right else x, y][0] / color_shades))

        if not end_at_right:
            for sample_index in range(0, 10):
                x_pos, y_pos = lerp_wave(val_band / 5, page_left + x * width_per_wave, page_top + y * 2.5, width_per_wave, sample_index/10)
                y_pos = y_pos / 1.4;
                last_x, last_y = x_pos, y_pos
                left_belt, right_belt = insutil.cartesian_to_belt(x_pos, y_pos, m_dist)
        
                left_belt_delta = left_belt - current_lbelt
                right_belt_delta = right_belt - current_rbelt
                ins.append([int(round(insutil.mm_to_steps(-left_belt_delta))), int(round(insutil.mm_to_steps(-right_belt_delta)))])
                current_lbelt = left_belt
                current_rbelt = right_belt
        else:
            for sample_index in range(0, 10):
                x_pos, y_pos = lerp_wave(val_band / 5, 190 + page_left - x * width_per_wave, page_top + y * 2.5, width_per_wave, 1 - sample_index/10)
                y_pos = y_pos / 1.4;
                last_x, last_y = x_pos, y_pos
                left_belt, right_belt = insutil.cartesian_to_belt(x_pos, y_pos, m_dist)
        
                left_belt_delta = left_belt - current_lbelt
                right_belt_delta = right_belt - current_rbelt
                ins.append([int(round(insutil.mm_to_steps(-left_belt_delta))), int(round(insutil.mm_to_steps(-right_belt_delta)))])
                current_lbelt = left_belt
                current_rbelt = right_belt

    for i in range(0, 10):
        x_pos, y_pos = lerp(last_x, last_y, last_x, last_y + 2.5, i/10)
        y_pos = y_pos / 1.4;
        left_belt, right_belt = insutil.cartesian_to_belt(x_pos, y_pos, m_dist)
        left_belt_delta = left_belt - current_lbelt
        right_belt_delta = right_belt - current_rbelt
        ins.append([int(round(insutil.mm_to_steps(-left_belt_delta))), int(round(insutil.mm_to_steps(-right_belt_delta)))])
        current_lbelt = left_belt
        current_rbelt = right_belt




"""
for x in range(0, 10):
    for y in range(0, 10):
        val = shrunk_pixels[x, i][0]
        val_band = int(round(val / color_shades))
        for i in range(10):
            x_pos, y_pos = lerp_wave(val_band, page_left + x * (val), y + page_top, 210, (i+1)/600)

            left_belt, right_belt = insutil.cartesian_to_belt(x_pos, y_pos, m_dist)
        
            left_belt_delta = left_belt - current_lbelt
            right_belt_delta = right_belt - current_rbelt
            ins.append([int(round(insutil.mm_to_steps(-left_belt_delta))), int(round(insutil.mm_to_steps(-right_belt_delta)))])
            current_lbelt = left_belt
            current_rbelt = right_belt
"""

insutil.write_instructions(ins)
