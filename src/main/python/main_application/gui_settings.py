class MonteCarloSettings:
    """
    Class is responsible for Monte Carlo algorithm settings.
    """
    def __init__(self):
        self.max_iterations = 30
        self.max_time = 4 * 1000
        self.max_moves_per_iteration = 25
        self.limit_iterations = True
        self.limit_moves = True
        self.exploration_parameter = 1.41

    def validate(self):
        """
        Validate if user introduces acceptable values:
        - max iterations in range [1; 10k]
        - max time per move in range [1000 ms; 120k ms]
        - moves per iteration in range [10; 100k]
        - exploration parameter in range [0; 20]
        :return: Message or empty string
        """
        if self.limit_moves and (self.max_moves_per_iteration < 10 or self.max_moves_per_iteration > 100000):
            return "Invalid moves limit. Should be between 10 and 100000."
        if self.limit_iterations and (self.max_iterations < 1 or self.max_iterations > 10000):
            return "Invalid iterations limit. Should be between 1 and 10000."
        elif not self.limit_iterations and (self.max_time < 1000 or self.max_time > 120000):
            return "Invalid time limit. Should be between 1s and 120s."
        elif self.exploration_parameter < 0 or self.exploration_parameter > 20:
            return "Invalid exploration parameter. Should be between 0 and 20."
        return ""

    def get_internal_time(self):
        return 0.9 * self.max_time


class DisplaySettings:
    """
    Class containing information about edge color-range and if animation is on.
    """
    def __init__(self):
        self.animate = False
        self.most_visited_color = (0, 255, 0, 255)
        self.least_visited_color = (255, 0, 0, 255)
