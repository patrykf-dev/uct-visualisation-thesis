class MonteCarloSettings:
    def __init__(self):
        self.max_iterations = 30
        self.max_time = 4 * 1000
        self.max_moves_per_iteration = 50
        self.limit_iterations = True
        self.limit_moves = True

    def validate(self):
        if self.limit_moves and (self.max_moves_per_iteration < 10 or self.max_moves_per_iteration > 100000):
            return "Invalid moves limit. Should be between 10 and 100000."

        if self.limit_iterations and (self.max_iterations < 1 or self.max_iterations > 10000):
            return "Invalid iterations limit. Should be between 1 and 10000."
        elif not self.limit_iterations and (self.max_time < 1000 or self.max_time > 30000):
            return "Invalid time limit. Should be between 1000 and 30000."
        return ""

    def get_internal_time(self):
        return 0.9 * self.max_time


class DisplaySettings:
    def __init__(self):
        self.animate = False