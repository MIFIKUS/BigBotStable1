def get_hwnd_from_list(accs_and_hwnds_list:list, server:str) -> int or bool:
    for i in accs_and_hwnds_list:
        print(i)
        server.lower()
        list(i.items())[0][1].lower()
        print(server.lower().find(list(i.items())[0][1].lower()))
        if server.lower().find(list(i.items())[0][1].lower()) >= 0:
            return list(i.items())[0][0]
    return False
