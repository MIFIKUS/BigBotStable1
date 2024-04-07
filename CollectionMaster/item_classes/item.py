class Item:
    def __init__(self):
        self.suitable_colors = ('Green', 'White')
        self.color = None
        self.ready_for_collection = None
        self.there_is_collections = None
        self.equipped = None
        self.sharped = None
        self.use_sharped_items = False
        self.safe_sharp_lvl = None

    def check_if_color_suitable(self):
        if self.color not in self.suitable_colors:
            return False
        return True

    def check_if_possible_to_use_sharp_items(self):
        if self.use_sharped_items is True:
            return True
        return False