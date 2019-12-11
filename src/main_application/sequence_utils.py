class MonteCarloNodeSequenceInfo:
    def __init__(self, root, filename):
        self.root = root
        self.filename = filename

    def __str__(self):
        return f"{self.filename}"
