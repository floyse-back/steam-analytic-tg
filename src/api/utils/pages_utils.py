


def page_utils_elements(callback_data:str,page_one_data:str):
    if callback_data == page_one_data:
        page = 1
    else:
        page = int(callback_data.split(":")[1])

    return page