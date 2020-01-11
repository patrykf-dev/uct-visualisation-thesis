class MonteCarloNodeDetails:
    def __init__(self):
        self.state_name = ""
        self.move_name = ""
        self.visits_count = 0
        self.visits_count_pre_modified = 0
        self.win_score = 0
        self.average_prize = 0

    def add_score(self, amount):
        self.win_score = self.win_score + amount
        self.average_prize = self.win_score / self.visits_count

    def mark_visit(self):
        self.visits_count = self.visits_count + 1
