import math

from insutil import PaperCanvas

x_margin = 20
start_x = x_margin
end_x = 210 - x_margin
x = start_x
y = 30
wave_samples = 400
rows = 60
noise_scale = 0.5

pc = PaperCanvas(x, y, (754 - 210) / 1.98, 192.0, 754)


for py in range(0, rows):

    for px in range(0, wave_samples):
        pc.goto(x, y + math.sin(x) * noise_scale)
        pc.sample()
        x += (1 / wave_samples) * (end_x - start_x)

    y += 1.1
    pc.goto(x, y)
    pc.sample()

    for px in range(0, wave_samples):
        pc.goto(x, y + math.sin(x) * noise_scale)
        pc.sample()
        x -= (1 / wave_samples) * (end_x - start_x)

    y += 1.1
    pc.goto(x, y)
    pc.sample()


"""
for h in range(0, 10):

    for i in range(0, wave_samples):
        pc.goto(x, y + land_function(i, wave_samples))
        print(y + math.sin(x))
        pc.sample()
        x += (1 / wave_samples) * (end_x - start_x)

    for i in range(0, 10):
        y += h / 10
        pc.goto(x, y)
        pc.sample()

    for i in range(0, wave_samples):
        pc.goto(x, y + land_function(wave_samples - 1 - i, wave_samples))
        print(y + math.sin(x))
        pc.sample()
        x -= (1 / wave_samples) * (end_x - start_x)

    for i in range(0, 10):
        y += h / 10
        pc.goto(x, y)
        pc.sample()
"""


ins = pc.gen_instructions()

with open("../sim-rs/ins.json", "w") as fp:
    fp.write(ins)
