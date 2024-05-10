import shutil


class BeautifyListofItems:
    def __init__(self, list_of_items):
        self._minimal_price_for_red = 300
        self._minimal_price_for_purple = 5000
        self._delimeter = 100
        self._purple_delimeter = 1000
        self._list_of_items = list_of_items
        self._colors = {
            'green': "\033[92m",
            'orange': "\033[93m",
            'red': "\033[91m",
            'purple': "\033[95m",
            'end': "\033[0m"
        }

    def _beautify_list(self) -> dict:
        items_string = {}
        for name_of_items, info_list in self._list_of_items.items():
            if info_list[0] <= self._minimal_price_for_red:
                if info_list[1]:
                    items_string.update({f"{self._colors['purple']}{name_of_items}{self._colors['end']}": f"{self._colors['green']}{info_list[0]}{self._colors['end']}"})
                else:
                    items_string.update({name_of_items: f"{self._colors['green']}{info_list}{self._colors['end']}"})

            elif info_list[0] >= self._minimal_price_for_red and info_list[0] <= self._minimal_price_for_red + self._delimeter:
                if info_list[1]:
                    items_string.update({f"{self._colors['purple']}{name_of_items}{self._colors['end']}": f"{self._colors['orange']}{info_list[0]}{self._colors['end']}"})
                else:
                    items_string.update({name_of_items: f"{self._colors['orange']}{info_list[0]}{self._colors['end']}"})

            else:
                if info_list[1]:
                    items_string.update({f"{self._colors['purple']}{name_of_items}{self._colors['end']}": f"{self._colors['red']}{info_list[0]}{self._colors['end']}"})
                else:
                    items_string.update({name_of_items: f"{self._colors['red']}{info_list[0]}{self._colors['end']}"})
        return items_string

    def print_beautify_list(self):
        list_of_items = self._beautify_list()
        max_key_length = max(map(len, (key for d in list_of_items for key in list_of_items.keys())))
        ready_string = ''
        for key, value in list_of_items.items():
            ready_string += f'{key.ljust(max_key_length)}: {str(value)}\n'
        print(ready_string, end='\n\n\n\n')



