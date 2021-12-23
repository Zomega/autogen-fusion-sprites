from os import walk, getcwd
from os.path import join
from PIL import Image
import imagehash


data_source = set()
path = "Japeal"
previous_filehash = None
previous_name = None

def add_element(element):
    data_source.add(element)


def is_fusion(name):
    return name.count('.') == 2


def is_duplicate(element):
    return element in data_source


def hash(filename):
    image = Image.open(filename)
    ch = imagehash.colorhash(image)               # meh
    ah = imagehash.average_hash(image)            # meh, but better
    ph = imagehash.phash(image)                   # nice
    dh = imagehash.dhash(image)                   # nice
    # crh = imagehash.crop_resistant_hash(image)  # complex
    return str(ah) + "/" + str(ch) + "/" + str(ph) + "/" + str(dh)


print(" ")
print("> START\n")
with open("fusions.txt", "w") as fusions:
    with open("duplicates2.txt", "w") as duplicates:
        for root, dirs, files in walk(path):
            for name in files:
                if name.endswith((".png")):
                    filename = join(getcwd(), root, name)
                    filehash = str(hash(filename))
                    fusions.write(name + " " + filehash + "\n")
                    if is_fusion(name):
                        if is_duplicate(filehash) and previous_filehash == filehash:
                            print(name, previous_name, filehash)
                            duplicates.write(f"{name} {previous_name} {filehash}\n")
                        else:
                            # print(name)
                            add_element(filehash)
                        previous_name = name
                        previous_filehash = filehash
print("\n> END")

