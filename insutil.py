import math


def get_ins_path():
    return "../sim-rs/ins.json"


def write_instructions(ins):
    str = "["
    for i in ins:
        lb = f"{round(-i[0], 0):.0f}"
        rb = f"{round(-i[1], 0):.0f}"
        str += f"[{0 if lb == "-0" else lb}, {0 if rb == "-0" else rb}],"

    str = str[:-1]
    str += "]"


    with open(get_ins_path(), "w") as fp:
        fp.write(str)


def cartesian_to_belt(x, y, motor_distance):
    left_belt = math.sqrt(x ** 2 + y ** 2)
    right_belt = math.sqrt((motor_distance - x) ** 2 + y ** 2)

    return (left_belt, right_belt)


def belt_to_cartesian(lb, rb, motor_distance):
    x = (motor_distance ** 2 + lb ** 2 - rb ** 2) / (2 * motor_distance)
    y = math.sqrt(lb ** 2 - x ** 2)

    return (x, y)

def mm_to_steps(mm):
    return mm * (3200 / (math.pi * 12.63))




class PaperCanvas:
    def __init__(self, init_x, init_y, left_motor_left_offset, left_motor_top_offset, motor_dist):
        self.current_x = init_x
        self.current_y = init_y
        self.delta_belts = []

        self.lm_h_offset = left_motor_left_offset
        self.lm_v_offset = left_motor_top_offset
        self.motor_dist = motor_dist

        self.lb, self.rb = cartesian_to_belt(self.current_x + self.lm_h_offset, self.current_y + self.lm_v_offset, motor_dist)
        self.sample() # sample initial position

    # moves the belts to a position, xy, on the page
    def goto(self, x, y):
        self.current_x = x
        self.current_y = y

    # goto, just for x
    def goto_x(self, x):
        self.current_x = x

    # goto, just for y
    def goto_y(self, y):
        self.current_y = y

    # sample a point at a given position, adding it to the instruction list
    def sample(self):
        lb, rb = cartesian_to_belt(self.current_x + self.lm_h_offset, self.current_y + self.lm_v_offset, self.motor_dist)
        # print(f"x:{self.current_x + self.lm_h_offset} y:{self.current_y + self.lm_v_offset}")
        
        delta_lb = lb - self.lb
        delta_rb = rb - self.rb
        # delta_lb = self.lb - lb
        # delta_rb = self.rb - rb

        delta_step_lb = round(mm_to_steps(delta_lb))
        delta_step_rb = -round(mm_to_steps(delta_rb))

        self.delta_belts.append((delta_step_lb, delta_step_rb))

        self.lb = lb
        self.rb = rb

    # takes the list of points and generates instructions to move between them
    def gen_instructions(self):
        deltas = []
        
        """
        for i in range(1, len(self.belt_lengths)):
            delta_x = self.belt_lengths[i][0] - self.belt_lengths[i - 1][0]
            delta_y = self.belt_lengths[i][1] - self.belt_lengths[i - 1][1]

            delta_x = round(mm_to_steps(delta_x))
            delta_y = round(mm_to_steps(delta_y))

            deltas.append((delta_x, delta_y))
        """
        
        delta_clone = self.delta_belts
        delta_clone.pop(0)
        delta_clone.pop(0)
        out = str(delta_clone)
        out = out.replace("(", "[")
        out = out.replace(")", "]")
        return out



