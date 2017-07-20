#methods
def file_read(self, file_id):
    img_array = io.imread(file_id)
    if (img_array.shape[2] == 4):
        img_array = img_array[:, :, :3]
    return img_array



def difference(descript, database):
    names = []
    # descript = a (128,) shape descriptor
    dict_least = dict()
    for key, val in database.items():
        dict_least[key] = np.sqrt((descript-val)**2)
    name_best = min(dict_least, key = d.get)
    if dict_least[key] > 0.5:
        return "No match found"
    else:
        return name_best



