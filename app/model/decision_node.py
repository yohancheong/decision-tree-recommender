class DecisionNode:
    """
        Decision node includes a condition to evaluate when making predictions, 
        and has connections to child branches
    """

    def __init__(self,
                condition,
                true_branch,
                false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch