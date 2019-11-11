class MonteCarloNodeVisualisationDetails:
    def __init__(self, depth=0):
        self.x = -1.0
        self.y = depth
        self.thread = None
        self.mod = 0
        self.ancestor = self
        self.change = 0
        self.shift = 0
