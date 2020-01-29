
class MonteCarloNodeDetails:
    """
    Class is responsible for storing information about Monte Carlo Tree Search properties of the node.
    """
    def __init__(self):
        self.state_name = ""
        self.move_name = ""
        self.visits_count = 0
        self.visits_count_pre_modified = 0
        self.win_score = 0
        self.average_prize = 0

    def add_score(self, amount):
        """
        Adds given amount to the win score.

		Args:
			amount:  numeric value

		Returns:
			None        
		"""
        self.win_score = self.win_score + amount
        self.average_prize = self.win_score / self.visits_count

    def mark_visit(self):
        """
        Increments counter of visits.

		Returns:
			None        
		"""
        self.visits_count = self.visits_count + 1

