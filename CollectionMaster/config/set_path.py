def set_path():
    with open('settings.txt') as f:
        for i in f.readlines():
            if 'path' in i:
                path = i.split('=')[1]
                return path + '\\CollectionMaster'