import app.config as config
from random import randint,shuffle
from app.service.decision_tree_service import DecisionTreeService

class OrderService(object):
    """
        Order Service to recommend menu options and make an order
    """

    menus_all = []
    menus_recommended = []
    menus_ordered = []

    def __init__(self, menus_all):
        
        self.menus_all = menus_all

        # Build decision tree using labels manually generated
        self.build_deicsion_tree()

    def make_order(self, max_menus_recommended, menu_previously_chosen=None, ask_again=False):
        """
            Make an order based on the recommended or random menu options
        """

        if not ask_again:

            self.menus_recommended = {}
            if menu_previously_chosen:

                # Recommend menus based on the user selection using a decision tree
                tree_input = menu_previously_chosen.get_tree_input()
                predictions = self.service.classify(tree_input, self.decision_tree)

                # Shuffle menus otherwise same set of menus will be shown in the next order
                shuffle(predictions)
                i = 0
                for p in predictions[:max_menus_recommended]:
                    self.menus_recommended[i] = self.menus_all[int(p[-2])]
                    self.menus_recommended[i].recommended = True
                    i += 1
                
            # Suggest random menus if we have less than max_menu_recommendataions e.g. 5
            menus_recommended_length = len(self.menus_recommended)
            if max_menus_recommended > menus_recommended_length:
                for i in range(menus_recommended_length, max_menus_recommended):
                    self.menus_recommended[i] = self.menus_all[randint(0, len(self.menus_all)-1)]

        str_builder = ''
        for k in self.menus_recommended:
            m = self.menus_recommended[k]
            str_builder += '\n{} - {} (meal: {}, protein: {}, veg: {}, gluten: {})'.format( \
                k, m.receipe_name, str(m.meal).lower(), str(m.protein2).lower(), str(m.vegetarian).lower(), str(m.gluten).lower())
            
            # Highlight recommended menus
            if m.recommended:
                str_builder += ' - RECOMMENDED!'

        option = input('\n>>> Choose one of menus with number (0-{}) or Quit (q):\n{}\n'.format(max_menus_recommended, '' if ask_again else str_builder))

        if option == 'q':

            # Show a list of menus ordered before terminating the program
            print('\n>>> Here is the list of menus ordered:')
            [print('- {}'.format(m.receipe_name)) for m in self.menus_ordered]
            exit()

        elif option in [str(i) for i in range(0, len(self.menus_recommended))]:

            # Store the chosen menus
            menu_selected = self.menus_recommended[int(option)]
            self.menus_ordered.append(menu_selected)
            self.make_order(max_menus_recommended, menu_previously_chosen=menu_selected)

        else:

            # Re-select an option
            self.make_order(max_menus_recommended, ask_again=True)

    def build_deicsion_tree(self):
        """
            Build decision tree
        """

        # Headers for model input arrays i.e. model features
        header = ['meal', 'protein2', 'vegetarian', 'gluten', 'label']

        # Prepare training dataset
        training_data = []
        for m in self.menus_all:
            training_data.append(m.get_tree_input())

        self.service = DecisionTreeService(header)
        self.decision_tree = self.service.build_tree(training_data)

        # Disply full decision tree 
        if config.DISPLAY_DECISION_TREE:
            self.service.print_tree(self.decision_tree)
            