
class Menu(object):
    """
        Menu object to contain details
    """

    id: str
    receipe_name: str
    servings: int
    calrories: int
    protetin: int
    fat: int
    carbs: int
    meal: str
    cuisine: str
    protein2: str
    vegetarian: bool
    gluten: bool
    label: str
    recommended: bool

    def __init__(self, 
                id, 
                receipe_name, 
                servings, 
                calrories,
                protein,
                fat,
                carbs,
                meal,
                cuisine,
                protein2,
                vegetarian,
                gluten):
        
        self.id = id
        self.receipe_name = receipe_name
        self.servings = servings
        self.calories = calrories
        self.protein = protein
        self.fat = fat
        self.carbs = carbs
        self.meal = meal
        self.cuisine = cuisine
        self.protein2 = protein2
        self.vegetarian = vegetarian
        self.gluten = gluten
        self.recommended = False

        # New label field is created since there is no label or class in a dataset to train a decision tree
        self.label = '-'.join([self.meal, self.protein2, 'V' if self.vegetarian else 'NV', 'G' if self.gluten else 'NG'])

    def get_tree_input(self):
        """
            Get model input array to train a decision tree
        """
        return [self.meal, self.protein2, self.vegetarian, self.gluten, self.id, self.label]


