#methods
def file_read(file_id):
    img_array = io.imread(r + file_id)
    if (img_array.shape[2] == 4):
        img_array = img_array[:, :, :3]
    return img_array


def difference(list_descriptors, database):
    dict_least = dict()
    for descript in list_descriptors:
        # descript = a (128,) shape descriptor
        for key, val in database.items(): """change this for dict items"""
            dict_least.add


