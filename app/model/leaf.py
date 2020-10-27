class Leaf:
    """
        Leaf node with menu items classified as similar or same
    """

    def __init__(self, rows, class_counts):
        self.predictions = rows
        self.class_counts = class_counts