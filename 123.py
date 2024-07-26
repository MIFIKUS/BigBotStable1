my_dict = {"a": 4, "b": 2, "c": 3}
sorted_dict = sorted(my_dict.items(), key=lambda x: x[1])
sorted_dict = {sorted_dict[0][0]: sorted_dict[0][1]}
print(sorted_dict)