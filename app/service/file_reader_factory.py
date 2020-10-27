from app.model.menu import Menu 

class FileReaderFactory(object):

    def __init__(self):
        pass

    def get_menus(self, file_path):

        results = []
        header_read = False
        with open(file_path, 'r') as f:

            if not header_read:
                header_read = True
            
            if header_read:
                for line in f:
                    c = line.split(';')
                    results.append(Menu(
                        c[0], 
                        c[1], 
                        c[2], 
                        c[3],
                        c[4], 
                        c[5], 
                        c[6], # Meal
                        c[7], 
                        c[8], # Protein2
                        c[9], 
                        True if c[10] == 'Yes' else False, # Vegetarian
                        True if c[11] == 'Yes' else False)) # Gluten

        return results

