import math
import random
import language_model
import permutation


class SimulatedAnnealing:

    def __init__(self, initial_temperature, threshold, cooling):
        self.initial_temperature = initial_temperature
        self.threshold = threshold
        self.cooling = cooling

    def get_temp(self):
        return self.initial_temperature

    def get_threshold(self):
        return self.threshold

    def get_cool(self):
        return self.cooling

    def run(self, h, d, model): # h - initial permutation, d - message
        t = self.get_temp()
        while t > self.get_threshold():
            h_tag = h.get_neighbor()
            delta = h_tag.get_energy(d, model)- h.get_energy(d, model)
            if delta < 0:
                p = 1
            else:
                p = math.exp((-delta)/ t)
            r = random.random()
            if r < p:
                h = h_tag
            t = t * self.get_cool()

        return h


