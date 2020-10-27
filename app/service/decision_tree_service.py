
import app.config as config
from app.model.condition import Condition
from app.model.leaf import Leaf
from app.model.decision_node import DecisionNode

class DecisionTreeService(object):
    """
        Service to build the best decision tree and make predictions
    """

    header = []

    def __init__(self, header):
        self.header = header

    def count_by_label(self, rows):
        """
            Count by label in a dataset
        """

        counts = {} 
        for row in rows:

            # The label is always the last column in our model input
            label = row[-1]
            if label not in counts:
                counts[label] = 0
            counts[label] += 1
        return counts

    def partition(self, rows, condition):
        """
            Evaluate the given condition with a row and partition to true vs false rows
        """
        true_rows, false_rows = [], []
        for row in rows:
            if condition.match(row):
                true_rows.append(row)
            else:
                false_rows.append(row)
        return true_rows, false_rows

    def compute_gini_index(self, rows):
        """
            Calculate impurity score for the given rows, 
            which shows how impure the a group of rows is. The lower, the puere.
            (For example, out of 14 menus, there are 9 pizzas and 5 sushies.
             Gini index = 1 - (9/14)^2 - (5/14)^2 = 0.46)
        """
        counts = self.count_by_label(rows)
        impurity = 1
        for lbl in counts:
            prob_of_lbl = counts[lbl] / float(len(rows))
            impurity -= prob_of_lbl**2
        return impurity

    def compute_info_gain(self, left_rows, right_rows, current_impurity):
        """
            Find information gain.
            The impurity of the starting node, minus the weighted impurity of two child nodes.
            The gain helps us to find a decision node which partition items purer.
        """
        p = float(len(left_rows)) / (len(left_rows) + len(right_rows))
        return current_impurity - p * self.compute_gini_index(left_rows) - (1 - p) * self.compute_gini_index(right_rows)

    def find_best_split(self, rows):
        """
            Find the best condition to ask on a node by iterating each feature (e.g. meal, protein2)
            and compute the information gain
        """
        best_gain = 0 
        best_condition = None 

        # Gini index on current node
        current_uncertainty = self.compute_gini_index(rows)

        # Number of feature columns (excluding id and label)
        n_features = len(rows[0]) - 2

        # For each feature
        for col in range(n_features):

            values = set([row[col] for row in rows])

            # For each unique value for the feature
            for val in values: 

                # Generate a condition
                condition = Condition(col, val, self.header)

                # Split rows with the condition
                true_rows, false_rows = self.partition(rows, condition)

                # Skip if the condition does not divide rows
                if len(true_rows) == 0 or len(false_rows) == 0:
                    continue

                # Calculate the information gain from this split
                gain = self.compute_info_gain(true_rows, false_rows, current_uncertainty)

                # Keep track of a condition with the highest gain (which makes child rows purer after patition)
                if gain >= best_gain:
                    best_gain, best_condition = gain, condition

        return best_gain, best_condition

    def build_tree(self, rows, current_depth=0):
        """
            Build decision tree
        """

        # Find the best condition to get the highest gain
        gain, condition = self.find_best_split(rows)

        # No more gain or reach to the max depth then terminate node growth
        if gain == 0 or current_depth >= config.DEPTH_DECISION_TREE:
            return Leaf(rows, self.count_by_label(rows))

        # Split rows to the left vs right nodes
        true_rows, false_rows = self.partition(rows, condition)

        current_depth = current_depth + 1

        # Recursively build the true branch
        true_branch = self.build_tree(true_rows, current_depth)

        # Recursively build the false branch
        false_branch = self.build_tree(false_rows, current_depth)

        # DecisionNode contains a complete child nodes and branches from the recursive calls
        return DecisionNode(condition, true_branch, false_branch)

    def classify(self, row, node):
        """
           Make predictions using the decision tree 
        """

        # If a node is leaf then make predictions
        if isinstance(node, Leaf):
            return node.predictions

        # If a condition is true then return predictions for true rows
        if node.condition.match(row):
            return self.classify(row, node.true_branch)
        else:
            return self.classify(row, node.false_branch)


    def print_tree(self, node, spacing=""):
        """
            Print a decision tree
        """

        if isinstance(node, Leaf):
            print (spacing + "Predict", node.predictions)
            return

        # Print the question at this node
        print (spacing + str(node.condition))

        # Call this function recursively on the true branch
        print (spacing + '--> True:')
        self.print_tree(node.true_branch, spacing + "  ")

        # Call this function recursively on the false branch
        print (spacing + '--> False:')
        self.print_tree(node.false_branch, spacing + "  ")

    def print_leaf(self, counts):
        """
            Print a leaf node with details
        """
        
        # Total number of menu items to return
        total = sum(counts.values()) * 1.0
        probs = {}

        # The number of menu items with same label in total
        for lbl in counts.keys():
            probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
        return probs
