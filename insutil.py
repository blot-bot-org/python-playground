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
    # init_x is the mm across the page, from top left
    # init_y is the mm down the page, from top left
    # left_motor_left_offset is the distance between the left motor wheel and edge of paper
    # left_motor_top_offset is the distance between the left motor wheel and top of paper
    # motor_dist is distance between left motor wheel and right motor wheel
    def __init__(self, init_x, init_y, left_motor_left_offset, left_motor_top_offset, motor_dist):
        self.last_x = init_x
        self.last_y = init_y
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
        self.goto_x(x)
        self.goto_y(y)

    # goto, just for x
    def goto_x(self, x):
        self.last_x = self.current_x
        self.current_x = x

    # goto, just for y
    def goto_y(self, y):
        self.last_y = self.current_y
        self.current_y = y

    # sample a point at a given position, adding the belt deltas to the instruction list
    def sample(self):
        # get belt lengths at new position
        lb, rb = cartesian_to_belt(self.current_x + self.lm_h_offset, self.current_y + self.lm_v_offset, self.motor_dist)
        # print(f"x:{self.current_x + self.lm_h_offset} y:{self.current_y + self.lm_v_offset}")
        
        # calculate the amount the belts moved, in mm
        delta_lb = lb - self.lb
        delta_rb = rb - self.rb

        # transform the mm belt deltas into steps for the stepper motors
        delta_step_lb = round(mm_to_steps(delta_lb))
        delta_step_rb = -round(mm_to_steps(delta_rb))

        # append the delta steps
        self.delta_belts.append((delta_step_lb, delta_step_rb))

        self.lb = lb
        self.rb = rb

    # this function is really bad it was make super scrappy(ily?), it should pop the last belt instructions, compute the length change and apply it
    # to the current_x/current_y. then i can NOT store the last_x and last_y
    def pop_sample(self):
        if(len(self.delta_belts)) > 0:
            self.delta_belts.pop()
            self.lb, self.rb = cartesian_to_belt(self.current_x + self.lm_h_offset, self.current_y + self.lm_v_offset, self.motor_dist)
            self.current_x = self.last_x
            self.current_y = self.last_y
        else:
            print("couldnt pop belt movement, no belt movements are on stack")

    # takes the list of points and generates instructions to move between them. for some reason i have to pop the first two, i could figure out why but all i know is that it works.
    def gen_instructions(self):
        delta_clone = self.delta_belts
        delta_clone.pop(0)
        delta_clone.pop(0)
        out = str(delta_clone)
        out = out.replace("(", "[")
        out = out.replace(")", "]")
        return out



