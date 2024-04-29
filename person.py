import math
import numpy as np


class Person:
    def __init__(self, i, pos_x, pos_y, target_x, target_y, v, t_recover, fixed):
        # movement speed
        self.v = v
        # target position
        self.target_x = target_x
        self.target_y = target_y
        # ID and name
        self.index = i
        self.name = "Person: " + str(i)
        # State: Susceptible, Infected or Retired
        self.infected = False
        self.susceptible = True
        self.retired = False
        # Current position
        self.pos_x = pos_x
        self.pos_y = pos_y
        # is it fixed (in quarantine)?
        self.fixed = fixed

        # displacement per iteration
        if self.fixed:

            self.delta_x = 0
            self.delta_y = 0
        else:
            self.delta_x = (self.target_x - self.pos_x) / self.v
            self.delta_y = (self.target_y - self.pos_y) / self.v
        # time in which the person was infected
        self.i_transmission = -1
        # time that the infection lasts, recover time
        self.t_recover = t_recover

    def __str__(self):
        return self.name + " in position " + str(self.pos_x) + ", " + str(self.pos_y)

    def infect(self, i):
        # infect
        self.infected = True
        self.susceptible = False
        self.retired = False
        self.i_transmission = i

    def retire(self):
        # heal
        self.retired = True
        self.susceptible = False
        self.infected = False

    def set_target(self, target_x, target_y):
        # this function is used to create a new target position
        self.target_x = target_x
        self.target_y = target_y
        if self.fixed:
            self.delta_x = 0
            self.delta_y = 0
        else:
            self.delta_x = (self.target_x - self.pos_x) / self.v
            self.delta_y = (self.target_y - self.pos_y) / self.v
        print("New target   ", self.target_x, self.target_y, "  ", self.index)

    def check_transmission(self, i):
        # this function is used to heal the person if the established infection time has passed
        if self.i_transmission > -1:
            if i - self.i_transmission > self.t_recover:
                self.retire()

    def update_pos(self, n_pos_x, n_posy):
        # this function animates the movement
        if n_pos_x == 0 and n_posy == 0:
            self.pos_x = self.pos_x + self.delta_x
            self.pos_y = self.pos_y + self.delta_y
        else:
            self.pos_x = n_pos_x
            self.pos_y = n_posy

        if abs(self.pos_x - self.target_x) < 3 and abs(self.pos_y - self.target_y) < 3:
            self.set_target(np.random.random() * 100, np.random.random() * 100)
        if self.pos_x > 100:
            self.pos_x = 100
        if self.pos_y > 100:
            self.pos_y = 100
        if self.pos_x < 0:
            self.pos_x = 0
        if self.pos_y < 0:
            self.pos_y = 0

    def get_color(self):
        if self.infected:
            return 'red'
        if self.susceptible:
            return 'blue'
        if self.retired:
            return 'gray'

    def get_pos(self):
        return self.pos_x, self.pos_y

    def get_dist(self, x, y):
        # this function calculates the distance between this person and another
        return math.sqrt((self.pos_x - x) ** 2 + (self.pos_y - y) ** 2)
